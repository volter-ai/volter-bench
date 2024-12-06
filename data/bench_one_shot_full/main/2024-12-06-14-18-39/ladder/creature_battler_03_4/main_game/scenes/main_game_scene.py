from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_chosen_skill = None
        self.opponent_chosen_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        # Type effectiveness
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf": multiplier = 2.0
            elif defender_creature.creature_type == "water": multiplier = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire": multiplier = 2.0
            elif defender_creature.creature_type == "leaf": multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water": multiplier = 2.0
            elif defender_creature.creature_type == "fire": multiplier = 0.5

        return int(raw_damage * multiplier)

    def execute_turn(self):
        # Determine order based on speed
        first = self.player
        second = self.opponent
        first_creature = self.player_creature
        second_creature = self.opponent_creature
        first_skill = self.player_chosen_skill
        second_skill = self.opponent_chosen_skill

        if second_creature.speed > first_creature.speed or \
           (second_creature.speed == first_creature.speed and random.random() < 0.5):
            first, second = second, first
            first_creature, second_creature = second_creature, first_creature
            first_skill, second_skill = second_skill, first_skill

        # Execute skills in order
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
        while True:
            # Player turn
            choices = [SelectThing(skill) for skill in self.player_creature.skills]
            self.player_chosen_skill = self._wait_for_choice(self.player, choices).thing

            # Opponent turn
            self.opponent_chosen_skill = self._wait_for_choice(self.opponent, 
                [SelectThing(skill) for skill in self.opponent_creature.skills]).thing

            # Execute turn
            self.execute_turn()

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")
