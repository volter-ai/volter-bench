from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_chosen_skill = None
        self.bot_chosen_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.bot.display_name}'s {self.bot_creature.display_name} (HP: {self.bot_creature.hp}/{self.bot_creature.max_hp})

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} type, {'Physical' if skill.is_physical else 'Special'})" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Calculate type effectiveness
        effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf":
                effectiveness = 2.0
            elif defender_creature.creature_type == "water":
                effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire":
                effectiveness = 2.0
            elif defender_creature.creature_type == "leaf":
                effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water":
                effectiveness = 2.0
            elif defender_creature.creature_type == "fire":
                effectiveness = 0.5

        return int(raw_damage * effectiveness)

    def get_skill_from_button_choice(self, creature, button_choice):
        # Find the skill in creature's skills that matches the button's display name
        for skill in creature.skills:
            if skill.display_name == button_choice.display_name:
                return skill
        raise ValueError(f"Could not find skill matching button {button_choice.display_name}")

    def execute_turn(self):
        # Determine order
        first = self.player
        second = self.bot
        first_creature = self.player_creature
        second_creature = self.bot_creature
        first_skill = self.player_chosen_skill
        second_skill = self.bot_chosen_skill

        if self.bot_creature.speed > self.player_creature.speed or \
           (self.bot_creature.speed == self.player_creature.speed and random.random() < 0.5):
            first, second = second, first
            first_creature, second_creature = second_creature, first_creature
            first_skill, second_skill = second_skill, first_skill

        # Execute moves
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
        self._show_text(self.player, f"Battle start! {self.player.display_name} VS {self.bot.display_name}")

        while True:
            # Player choice phase
            skill_buttons = [Button(skill.display_name) for skill in self.player_creature.skills]
            choice = self._wait_for_choice(self.player, skill_buttons)
            self.player_chosen_skill = self.get_skill_from_button_choice(self.player_creature, choice)

            # Bot choice phase
            bot_choice = self._wait_for_choice(self.bot, 
                [Button(skill.display_name) for skill in self.bot_creature.skills])
            self.bot_chosen_skill = self.get_skill_from_button_choice(self.bot_creature, bot_choice)

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
