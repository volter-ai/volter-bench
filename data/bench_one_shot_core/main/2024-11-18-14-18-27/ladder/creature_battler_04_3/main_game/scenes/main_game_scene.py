from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
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

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Opponent's {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        # Calculate base damage
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

    def execute_turn(self, first_creature, second_creature, first_skill, second_skill):
        # First attack
        damage = self.calculate_damage(first_creature, second_creature, first_skill)
        second_creature.hp -= damage
        self._show_text(self.player, f"{first_creature.display_name} used {first_skill.display_name} for {damage} damage!")
        
        # Check if battle ended
        if second_creature.hp <= 0:
            return
            
        # Second attack
        damage = self.calculate_damage(second_creature, first_creature, second_skill)
        first_creature.hp -= damage
        self._show_text(self.player, f"{second_creature.display_name} used {second_skill.display_name} for {damage} damage!")

    def run(self):
        while True:
            # Player choice
            skill_choices = [DictionaryChoice(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            player_skill = self.player_creature.skills[skill_choices.index(player_choice)]

            # Bot choice
            bot_skill_choices = [DictionaryChoice(skill.display_name) for skill in self.bot_creature.skills]
            bot_choice = self._wait_for_choice(self.bot, bot_skill_choices)
            bot_skill = self.bot_creature.skills[bot_skill_choices.index(bot_choice)]

            # Determine order
            if self.player_creature.speed > self.bot_creature.speed:
                first = (self.player_creature, self.bot_creature, player_skill, bot_skill)
            elif self.bot_creature.speed > self.player_creature.speed:
                first = (self.bot_creature, self.player_creature, bot_skill, player_skill)
            else:
                if random.random() < 0.5:
                    first = (self.player_creature, self.bot_creature, player_skill, bot_skill)
                else:
                    first = (self.bot_creature, self.player_creature, bot_skill, player_skill)

            self.execute_turn(*first)

            # Check win conditions
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        self._transition_to_scene("MainMenuScene")
