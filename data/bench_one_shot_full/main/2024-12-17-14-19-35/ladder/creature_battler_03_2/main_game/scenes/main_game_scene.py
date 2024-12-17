from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        # Type effectiveness
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf": multiplier = 2.0
            elif defender_creature.creature_type == "water": multiplier = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire": multiplier = 2.0
            elif defender_creature.creature_type == "leaf": multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water": multiplier = 2.0
            elif defender_creature.creature_type == "fire": multiplier = 0.5

        return int(raw_damage * multiplier)

    def execute_turn(self, first_creature, second_creature, first_skill, second_skill):
        # First attack
        damage = self.calculate_damage(first_creature, second_creature, first_skill)
        second_creature.hp -= damage
        self._show_text(self.player, f"{first_creature.display_name} used {first_skill.display_name} for {damage} damage!")
        
        # Second attack if still alive
        if second_creature.hp > 0:
            damage = self.calculate_damage(second_creature, first_creature, second_skill)
            first_creature.hp -= damage
            self._show_text(self.player, f"{second_creature.display_name} used {second_skill.display_name} for {damage} damage!")

    def run(self):
        while True:
            # Player choice phase
            choices = [SelectThing(skill) for skill in self.player_creature.skills]
            player_skill = self._wait_for_choice(self.player, choices).thing

            # Bot choice phase
            bot_skill = self._wait_for_choice(self.bot, [SelectThing(skill) for skill in self.bot_creature.skills]).thing

            # Determine order
            if self.player_creature.speed > self.bot_creature.speed:
                first, second = self.player_creature, self.bot_creature
                first_skill, second_skill = player_skill, bot_skill
            elif self.bot_creature.speed > self.player_creature.speed:
                first, second = self.bot_creature, self.player_creature
                first_skill, second_skill = bot_skill, player_skill
            else:
                if random.random() < 0.5:
                    first, second = self.player_creature, self.bot_creature
                    first_skill, second_skill = player_skill, bot_skill
                else:
                    first, second = self.bot_creature, self.player_creature
                    first_skill, second_skill = bot_skill, player_skill

            # Execute turn
            self.execute_turn(first, second, first_skill, second_skill)

            # Check win condition
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._transition_to_scene("MainMenuScene")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._transition_to_scene("MainMenuScene")
                break
