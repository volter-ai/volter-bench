from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_chosen_skill = None
        self.bot_chosen_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Type: {self.player_creature.creature_type}

VS

{self.bot.display_name}'s {self.bot_creature.display_name}
HP: {self.bot_creature.hp}/{self.bot_creature.max_hp}
Type: {self.bot_creature.creature_type}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.bot_creature.display_name}")
        
        while True:
            # Player Choice Phase
            self.player_chosen_skill = self._handle_player_turn()
            
            # Bot Choice Phase
            self.bot_chosen_skill = self._handle_bot_turn()
            
            # Resolution Phase
            self._resolve_turn()
            
            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
                
        self._transition_to_scene("MainMenuScene")

    def _handle_player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _handle_bot_turn(self):
        choices = [SelectThing(skill) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        return choice.thing

    def _calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Calculate type effectiveness
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf":
                multiplier = 2.0
            elif defender.creature_type == "water":
                multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire":
                multiplier = 2.0
            elif defender.creature_type == "leaf":
                multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water":
                multiplier = 2.0
            elif defender.creature_type == "fire":
                multiplier = 0.5
                
        return int(raw_damage * multiplier)

    def _resolve_turn(self):
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

        # First attack
        damage = self._calculate_damage(first_creature, second_creature, first_skill)
        second_creature.hp -= damage
        self._show_text(self.player, f"{first_creature.display_name} used {first_skill.display_name} for {damage} damage!")

        # Second attack if still alive
        if second_creature.hp > 0:
            damage = self._calculate_damage(second_creature, first_creature, second_skill)
            first_creature.hp -= damage
            self._show_text(self.player, f"{second_creature.display_name} used {second_skill.display_name} for {damage} damage!")
