from mini_game_engine.engine.lib import AbstractGameScene, Button, create_from_game_database
from main_game.models import Player
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        
        # Reset creature stats
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        
        self.player_choice = None
        self.bot_choice = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage
            
        # Calculate type multiplier
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

    def execute_turn(self):
        # Determine order
        first = self.player
        second = self.bot
        first_creature = self.player_creature
        second_creature = self.bot_creature
        first_skill = self.player_choice
        second_skill = self.bot_choice
        
        if self.bot_creature.speed > self.player_creature.speed or \
           (self.bot_creature.speed == self.player_creature.speed and random.random() < 0.5):
            first, second = second, first
            first_creature, second_creature = second_creature, first_creature
            first_skill, second_skill = second_skill, first_skill

        # Execute skills
        for attacker, defender, attacker_creature, defender_creature, skill in [
            (first, second, first_creature, second_creature, first_skill),
            (second, first, second_creature, first_creature, second_skill)
        ]:
            if defender_creature.hp > 0:  # Only attack if defender still alive
                damage = self.calculate_damage(attacker_creature, defender_creature, skill)
                defender_creature.hp = max(0, defender_creature.hp - damage)
                self._show_text(self.player, 
                    f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}! "
                    f"Dealt {damage} damage to {defender.display_name}'s {defender_creature.display_name}!")

    def run(self):
        while True:
            # Player choice phase
            skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            self.player_choice = next(s for s in self.player_creature.skills 
                                    if s.display_name == player_choice.display_name)
            
            # Bot choice phase
            bot_choice = self._wait_for_choice(self.bot, 
                [Button(skill.display_name) for skill in self.bot_creature.skills])
            self.bot_choice = next(s for s in self.bot_creature.skills 
                                 if s.display_name == bot_choice.display_name)
            
            # Resolution phase
            self.execute_turn()
            
            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
                
        self._transition_to_scene("MainMenuScene")
