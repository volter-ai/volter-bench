from mini_game_engine.engine.lib import AbstractGameScene, Button
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
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player phase
            self.player_phase()
            
            # Bot phase
            self.bot_phase()
            
            # Resolution phase
            if self.resolution_phase():
                break

    def player_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.queued_skills[self.player.uid] = self.player_creature.skills[choices.index(choice)]

    def bot_phase(self):
        choices = [Button(skill.display_name) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        self.queued_skills[self.bot.uid] = self.bot_creature.skills[choices.index(choice)]

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        # Type effectiveness
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

        # Execute moves
        for attacker in [first, second]:
            if attacker == self.player:
                damage = self.calculate_damage(self.player_creature, self.bot_creature, self.queued_skills[attacker.uid])
                self.bot_creature.hp -= damage
                self._show_text(self.player, f"{self.player_creature.display_name} used {self.queued_skills[attacker.uid].display_name} for {damage} damage!")
                
                if self.bot_creature.hp <= 0:
                    self._show_text(self.player, "You won!")
                    self._transition_to_scene("MainMenuScene")
                    return True
            else:
                damage = self.calculate_damage(self.bot_creature, self.player_creature, self.queued_skills[attacker.uid])
                self.player_creature.hp -= damage
                self._show_text(self.player, f"{self.bot_creature.display_name} used {self.queued_skills[attacker.uid].display_name} for {damage} damage!")
                
                if self.player_creature.hp <= 0:
                    self._show_text(self.player, "You lost!")
                    self._transition_to_scene("MainMenuScene") 
                    return True
                    
        return False
