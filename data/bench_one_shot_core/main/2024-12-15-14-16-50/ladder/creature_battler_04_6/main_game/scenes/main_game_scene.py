from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_skills = {}  # Will use player.uid as key instead of player object

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.bot.display_name}'s {self.bot_creature.display_name} (HP: {self.bot_creature.hp}/{self.bot_creature.max_hp})

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            self.player_choice_phase()
            
            # Bot Choice Phase  
            self.bot_choice_phase()
            
            # Resolution Phase
            if self.resolution_phase():
                break

        # Reset creatures before exiting
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [DictionaryChoice(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.queued_skills[self.player.uid] = next(s for s in self.player_creature.skills 
                                                  if s.display_name == choice.display_name)

    def bot_choice_phase(self):
        choices = [DictionaryChoice(skill.display_name) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        self.queued_skills[self.bot.uid] = next(s for s in self.bot_creature.skills 
                                               if s.display_name == choice.display_name)

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Calculate type multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf":
                multiplier = 2.0
            elif defender_creature.creature_type == "water":
                multiplier = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire":
                multiplier = 2.0
            elif defender_creature.creature_type == "leaf":
                multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water":
                multiplier = 2.0
            elif defender_creature.creature_type == "fire":
                multiplier = 0.5

        return int(raw_damage * multiplier)

    def resolution_phase(self):
        # Determine order
        first = self.player
        second = self.bot
        if self.bot_creature.speed > self.player_creature.speed:
            first, second = second, first
        elif self.bot_creature.speed == self.player_creature.speed:
            if random.random() < 0.5:
                first, second = second, first

        # Execute skills
        for attacker in [first, second]:
            defender = self.bot if attacker == self.player else self.player
            attacker_creature = self.player_creature if attacker == self.player else self.bot_creature
            defender_creature = self.bot_creature if attacker == self.player else self.player_creature
            
            skill = self.queued_skills[attacker.uid]  # Use uid instead of player object
            damage = self.calculate_damage(attacker_creature, defender_creature, skill)
            defender_creature.hp = max(0, defender_creature.hp - damage)
            
            self._show_text(self.player, 
                f"{attacker_creature.display_name} used {skill.display_name}! Dealt {damage} damage!")

            if defender_creature.hp <= 0:
                winner = "You win!" if defender == self.bot else "You lose!"
                self._show_text(self.player, winner)
                return True

        return False
