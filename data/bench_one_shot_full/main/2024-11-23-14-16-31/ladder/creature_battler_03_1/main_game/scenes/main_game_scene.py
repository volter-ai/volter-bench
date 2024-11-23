from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
from typing import Tuple

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_chosen_skill = None
        self.bot_chosen_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} - {skill.base_damage} damage)" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, attacker_creature, defender_creature, skill) -> int:
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        type_multiplier = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf": type_multiplier = 2.0
            elif defender_creature.creature_type == "water": type_multiplier = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire": type_multiplier = 2.0
            elif defender_creature.creature_type == "leaf": type_multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water": type_multiplier = 2.0
            elif defender_creature.creature_type == "fire": type_multiplier = 0.5

        return int(raw_damage * type_multiplier)

    def execute_turn(self) -> Tuple[bool, bool]:
        # Determine order
        first = self.player
        second = self.bot
        first_creature = self.player_creature
        second_creature = self.bot_creature
        first_skill = self.player_chosen_skill
        second_skill = self.bot_chosen_skill

        if second_creature.speed > first_creature.speed or \
           (second_creature.speed == first_creature.speed and random.random() < 0.5):
            first, second = second, first
            first_creature, second_creature = second_creature, first_creature
            first_skill, second_skill = second_skill, first_skill

        # Execute skills
        damage = self.calculate_damage(first_creature, second_creature, first_skill)
        second_creature.hp -= damage
        self._show_text(self.player, f"{first.display_name}'s {first_creature.display_name} used {first_skill.display_name} for {damage} damage!")
        
        if second_creature.hp <= 0:
            return first == self.player, True

        damage = self.calculate_damage(second_creature, first_creature, second_skill)
        first_creature.hp -= damage
        self._show_text(self.player, f"{second.display_name}'s {second_creature.display_name} used {second_skill.display_name} for {damage} damage!")

        if first_creature.hp <= 0:
            return second == self.player, True

        return False, False

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player.display_name} vs {self.bot.display_name}")

        while True:
            # Player choice phase
            choices = [SelectThing(skill) for skill in self.player_creature.skills]
            self.player_chosen_skill = self._wait_for_choice(self.player, choices).thing

            # Bot choice phase
            self.bot_chosen_skill = self._wait_for_choice(self.bot, 
                [SelectThing(skill) for skill in self.bot_creature.skills]).thing

            # Resolution phase
            player_won, battle_ended = self.execute_turn()

            if battle_ended:
                if player_won:
                    self._show_text(self.player, "You won!")
                else:
                    self._show_text(self.player, "You lost!")
                self._transition_to_scene("MainMenuScene")
                return
