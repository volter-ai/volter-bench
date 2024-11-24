from mini_game_engine.engine.lib import AbstractGameScene, Button
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
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Foe {self.bot_creature.display_name}: {self.bot_creature.hp}/{self.bot_creature.max_hp} HP

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
        # Determine order
        first = self.player_creature if self.player_creature.speed > self.bot_creature.speed else self.bot_creature
        second = self.bot_creature if first == self.player_creature else self.player_creature
        first_skill = player_skill if first == self.player_creature else bot_skill
        second_skill = bot_skill if first == self.player_creature else player_skill

        # If speeds are equal, randomize
        if self.player_creature.speed == self.bot_creature.speed:
            if random.random() < 0.5:
                first, second = second, first
                first_skill, second_skill = second_skill, first_skill

        # Execute first attack
        if first == self.player_creature:
            damage = self.calculate_damage(self.player_creature, self.bot_creature, first_skill)
            self.bot_creature.hp -= damage
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {first_skill.display_name}! Dealt {damage} damage!")
        else:
            damage = self.calculate_damage(self.bot_creature, self.player_creature, first_skill)
            self.player_creature.hp -= damage
            self._show_text(self.player, f"Foe's {self.bot_creature.display_name} used {first_skill.display_name}! Dealt {damage} damage!")

        # Check if battle is over
        if self.player_creature.hp <= 0 or self.bot_creature.hp <= 0:
            return

        # Execute second attack
        if second == self.player_creature:
            damage = self.calculate_damage(self.player_creature, self.bot_creature, second_skill)
            self.bot_creature.hp -= damage
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {second_skill.display_name}! Dealt {damage} damage!")
        else:
            damage = self.calculate_damage(self.bot_creature, self.player_creature, second_skill)
            self.player_creature.hp -= damage
            self._show_text(self.player, f"Foe's {self.bot_creature.display_name} used {second_skill.display_name}! Dealt {damage} damage!")

    def run(self):
        while True:
            # Player choice phase
            player_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, player_choices)
            player_skill = next(s for s in self.player_creature.skills if s.display_name == player_choice.display_name)

            # Bot choice phase
            bot_choice = self._wait_for_choice(self.bot, [Button(skill.display_name) for skill in self.bot_creature.skills])
            bot_skill = next(s for s in self.bot_creature.skills if s.display_name == bot_choice.display_name)

            # Resolution phase
            self.execute_turn(player_skill, bot_skill)

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene") 
                return
