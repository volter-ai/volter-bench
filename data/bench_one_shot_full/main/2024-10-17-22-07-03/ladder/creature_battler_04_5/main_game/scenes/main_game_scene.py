from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Player's turn:
> {self.player_creature.skills[0].display_name}
> {self.player_creature.skills[1].display_name}
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

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_turn(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolve_turn(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            first, second = (self.player, self.player_creature, player_skill), (self.opponent, self.opponent_creature, opponent_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            first, second = (self.opponent, self.opponent_creature, opponent_skill), (self.player, self.player_creature, player_skill)
        else:
            # If speeds are equal, randomly choose who goes first
            creatures = [(self.player, self.player_creature, player_skill), (self.opponent, self.opponent_creature, opponent_skill)]
            first, second = random.sample(creatures, k=2)

        self.execute_skill(*first, second[1])
        if second[1].hp > 0:
            self.execute_skill(*second, first[1])

    def execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        effectiveness = self.get_effectiveness(skill.skill_type, defender_creature.creature_type)
        final_damage = int(effectiveness * raw_damage)
        
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"It dealt {final_damage} damage to {defender_creature.display_name}!")

    def get_effectiveness(self, skill_type, creature_type):
        effectiveness_chart = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1)

    def check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
