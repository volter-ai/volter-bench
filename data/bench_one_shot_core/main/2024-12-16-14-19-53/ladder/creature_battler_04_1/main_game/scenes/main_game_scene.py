from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.reset_creatures()

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Foe {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Calculate type multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": multiplier = 2.0
            elif defender.creature_type == "water": multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": multiplier = 2.0
            elif defender.creature_type == "leaf": multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": multiplier = 2.0
            elif defender.creature_type == "fire": multiplier = 0.5

        return int(raw_damage * multiplier)

    def execute_turn(self, player_skill, bot_skill):
        # Determine order based on speed with random tiebreaker
        if self.player_creature.speed > self.bot_creature.speed:
            first = self.player_creature
            second = self.bot_creature
            first_skill = player_skill
            second_skill = bot_skill
        elif self.player_creature.speed < self.bot_creature.speed:
            first = self.bot_creature
            second = self.player_creature
            first_skill = bot_skill
            second_skill = player_skill
        else:
            # Random tiebreaker when speeds are equal
            if random.random() < 0.5:
                first = self.player_creature
                second = self.bot_creature
                first_skill = player_skill
                second_skill = bot_skill
            else:
                first = self.bot_creature
                second = self.player_creature
                first_skill = bot_skill
                second_skill = player_skill

        # Execute skills in determined order
        if first == self.player_creature:
            damage = self.calculate_damage(self.player_creature, self.bot_creature, first_skill)
            self.bot_creature.hp -= damage
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {first_skill.display_name}! Dealt {damage} damage!")
            
            if self.bot_creature.hp > 0:
                damage = self.calculate_damage(self.bot_creature, self.player_creature, second_skill)
                self.player_creature.hp -= damage
                self._show_text(self.player, f"Foe's {self.bot_creature.display_name} used {second_skill.display_name}! Dealt {damage} damage!")
        else:
            damage = self.calculate_damage(self.bot_creature, self.player_creature, first_skill)
            self.player_creature.hp -= damage
            self._show_text(self.player, f"Foe's {self.bot_creature.display_name} used {first_skill.display_name}! Dealt {damage} damage!")
            
            if self.player_creature.hp > 0:
                damage = self.calculate_damage(self.player_creature, self.bot_creature, second_skill)
                self.bot_creature.hp -= damage
                self._show_text(self.player, f"Your {self.player_creature.display_name} used {second_skill.display_name}! Dealt {damage} damage!")

    def run(self):
        self._show_text(self.player, f"A wild {self.bot_creature.display_name} appeared!")

        while True:
            # Player choice phase
            skill_choices = [DictionaryChoice(skill.display_name) for skill in self.player_creature.skills]
            player_skill = self.player_creature.skills[skill_choices.index(self._wait_for_choice(self.player, skill_choices))]

            # Bot choice phase
            bot_skill = self.bot_creature.skills[random.randint(0, len(self.bot_creature.skills)-1)]

            # Resolution phase
            self.execute_turn(player_skill, bot_skill)

            # Check win condition
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene") 
                break
