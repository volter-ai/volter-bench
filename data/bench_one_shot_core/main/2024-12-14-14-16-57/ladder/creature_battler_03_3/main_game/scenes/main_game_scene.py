from mini_game_engine.engine.lib import AbstractGameScene, Button
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

    def calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        type_multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": type_multiplier = 2.0
            elif defender.creature_type == "water": type_multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": type_multiplier = 2.0
            elif defender.creature_type == "leaf": type_multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": type_multiplier = 2.0
            elif defender.creature_type == "fire": type_multiplier = 0.5
            
        return int(raw_damage * type_multiplier)

    def execute_turn(self, first, second, first_skill, second_skill):
        # First attack
        damage = self.calculate_damage(first, second, first_skill)
        second.hp -= damage
        self._show_text(self.player, f"{first.display_name} used {first_skill.display_name} for {damage} damage!")
        
        if second.hp <= 0:
            return
            
        # Second attack
        damage = self.calculate_damage(second, first, second_skill)
        first.hp -= damage
        self._show_text(self.player, f"{second.display_name} used {second_skill.display_name} for {damage} damage!")

    def run(self):
        while True:
            # Player choice
            skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            player_skill = next(s for s in self.player_creature.skills if s.display_name == player_choice.display_name)

            # Bot choice
            bot_choice = self._wait_for_choice(self.bot, [Button(skill.display_name) for skill in self.bot_creature.skills])
            bot_skill = next(s for s in self.bot_creature.skills if s.display_name == bot_choice.display_name)

            # Determine order
            if self.player_creature.speed > self.bot_creature.speed:
                first, second = self.player_creature, self.bot_creature
                first_skill, second_skill = player_skill, bot_skill
            elif self.player_creature.speed < self.bot_creature.speed:
                first, second = self.bot_creature, self.player_creature
                first_skill, second_skill = bot_skill, player_skill
            else:
                if random.random() < 0.5:
                    first, second = self.player_creature, self.bot_creature
                    first_skill, second_skill = player_skill, bot_skill
                else:
                    first, second = self.bot_creature, self.player_creature
                    first_skill, second_skill = bot_skill, player_skill

            self.execute_turn(first, second, first_skill, second_skill)

            # Check win condition
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._transition_to_scene("MainMenuScene")
                return
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._transition_to_scene("MainMenuScene") 
                return
