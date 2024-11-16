from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}:
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Type: {self.player_creature.creature_type}

{self.bot.display_name}'s {self.bot_creature.display_name}:
HP: {self.bot_creature.hp}/{self.bot_creature.max_hp}
Type: {self.bot_creature.creature_type}
"""

    def calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Calculate type effectiveness
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

    def execute_turn(self, first_creature, first_skill, second_creature, second_skill):
        # First attack
        damage = self.calculate_damage(first_creature, second_creature, first_skill)
        second_creature.hp -= damage
        self._show_text(self.player, f"{first_creature.display_name} used {first_skill.display_name}! Dealt {damage} damage!")
        
        # Check if battle ended
        if second_creature.hp <= 0:
            return True
            
        # Second attack
        damage = self.calculate_damage(second_creature, first_creature, second_skill)
        first_creature.hp -= damage
        self._show_text(self.player, f"{second_creature.display_name} used {second_skill.display_name}! Dealt {damage} damage!")
        
        return first_creature.hp <= 0

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Choose your skill:")
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing

            # Bot choice phase
            bot_skill = self._wait_for_choice(self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]).thing

            # Resolution phase - determine order by speed
            battle_ended = False
            if self.player_creature.speed > self.bot_creature.speed or \
               (self.player_creature.speed == self.bot_creature.speed and random.random() < 0.5):
                battle_ended = self.execute_turn(self.player_creature, player_skill, 
                                              self.bot_creature, bot_skill)
            else:
                battle_ended = self.execute_turn(self.bot_creature, bot_skill,
                                              self.player_creature, player_skill)

            # Check win condition
            if battle_ended:
                if self.bot_creature.hp <= 0:
                    self._show_text(self.player, "You won!")
                else:
                    self._show_text(self.player, "You lost!")
                self._quit_whole_game()
