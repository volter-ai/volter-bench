from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_skill = None
        self.bot_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} - {skill.description}" for skill in self.player_creature.skills])}
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

    def execute_turn(self):
        # Determine order
        first = self.player
        second = self.bot
        first_creature = self.player_creature
        second_creature = self.bot_creature
        first_skill = self.player_skill
        second_skill = self.bot_skill

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
            if defender_creature.hp <= 0:
                continue
                
            damage = self.calculate_damage(attacker_creature, defender_creature, skill)
            defender_creature.hp = max(0, defender_creature.hp - damage)
            
            self._show_text(self.player, 
                f"{attacker_creature.display_name} used {skill.display_name}! "
                f"Dealt {damage} damage to {defender_creature.display_name}!")

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player.display_name} vs {self.bot.display_name}")

        while True:
            # Player choice phase
            choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
            choice = self._wait_for_choice(self.player, choices)
            self.player_skill = choice.thing

            # Bot choice phase
            bot_choices = [SelectThing(skill, label=skill.display_name) for skill in self.bot_creature.skills]
            self.bot_skill = self._wait_for_choice(self.bot, bot_choices).thing

            # Resolution phase
            self.execute_turn()

            # Check win condition
            if self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        # Reset creatures before leaving
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")
