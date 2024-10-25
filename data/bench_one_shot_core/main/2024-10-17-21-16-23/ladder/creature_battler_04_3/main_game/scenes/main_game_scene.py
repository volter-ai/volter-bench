from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while True:
            # Player turn
            player_skill = self.player_turn()
            
            # Opponent turn
            opponent_skill = self.opponent_turn()
            
            # Resolve turn
            self.resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            if self.check_battle_end():
                break

        # Reset creatures' state before transitioning
        self.reset_creatures_state()
        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_turn(self):
        return random.choice(self.opponent_creature.skills)

    def resolve_turn(self, player_skill, opponent_skill):
        first, second = self.determine_turn_order(player_skill, opponent_skill)
        self.execute_skill(*first)
        if not self.check_battle_end():
            self.execute_skill(*second)

    def determine_turn_order(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, player_skill, self.opponent_creature), (self.opponent, opponent_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, opponent_skill, self.player_creature), (self.player, player_skill, self.opponent_creature)
        else:
            if random.random() < 0.5:
                return (self.player, player_skill, self.opponent_creature), (self.opponent, opponent_skill, self.player_creature)
            else:
                return (self.opponent, opponent_skill, self.player_creature), (self.player, player_skill, self.opponent_creature)

    def execute_skill(self, attacker, skill, target):
        if skill.is_physical:
            raw_damage = attacker.creatures[0].attack + skill.base_damage - target.defense
        else:
            raw_damage = (attacker.creatures[0].sp_attack / target.sp_defense) * skill.base_damage

        effectiveness = self.calculate_effectiveness(skill.skill_type, target.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        target.hp = max(0, target.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.creatures[0].display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage to {target.display_name}!")

    def calculate_effectiveness(self, skill_type, target_type):
        effectiveness_chart = {
            "normal": {"fire": 1, "water": 1, "leaf": 1},
            "fire": {"fire": 1, "water": 0.5, "leaf": 2},
            "water": {"fire": 2, "water": 1, "leaf": 0.5},
            "leaf": {"fire": 0.5, "water": 2, "leaf": 1}
        }
        return effectiveness_chart.get(skill_type, {}).get(target_type, 1)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You won the battle!")
            return True
        return False

    def reset_creatures_state(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
        self._show_text(self.player, "All creatures have been restored to full health.")
