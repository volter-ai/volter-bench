from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player.display_name} vs {self.opponent.display_name}")
        self.battle_loop()

    def battle_loop(self):
        while not self.battle_ended:
            # Player turn
            player_skill = self.player_turn()
            
            # Opponent turn
            opponent_skill = self.opponent_turn()
            
            # Resolve turn
            self.resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            self.check_battle_end()

    def player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_turn(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolve_turn(self, player_skill, opponent_skill):
        first, second = self.determine_turn_order(player_skill, opponent_skill)
        self.execute_skill(*first)
        if not self.battle_ended:
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

    def execute_skill(self, attacker, skill, defender):
        if skill.is_physical:
            raw_damage = attacker.creatures[0].attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.creatures[0].sp_attack / defender.sp_defense) * skill.base_damage
        
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.creatures[0].display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender.display_name} took {final_damage} damage!")

    def calculate_weakness_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
            self.battle_ended = True
            self.reset_creatures_state()
            self._transition_to_scene("MainMenuScene")
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
            self.battle_ended = True
            self.reset_creatures_state()
            self._transition_to_scene("MainMenuScene")

    def reset_creatures_state(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
        self._show_text(self.player, "All creatures have been restored to full health.")
