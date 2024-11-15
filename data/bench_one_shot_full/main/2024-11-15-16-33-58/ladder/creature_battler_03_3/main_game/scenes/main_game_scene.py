from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_choice = None
        self.opponent_choice = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Calculate type effectiveness
        effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": effectiveness = 2.0
            elif defender.creature_type == "water": effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": effectiveness = 2.0
            elif defender.creature_type == "leaf": effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": effectiveness = 2.0
            elif defender.creature_type == "fire": effectiveness = 0.5

        return int(raw_damage * effectiveness)

    def run(self):
        while True:
            # Player choice phase
            choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, choices)
            self.player_choice = next(s for s in self.player_creature.skills 
                                    if s.display_name == player_choice.display_name)

            # Opponent choice phase
            opponent_choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
            opponent_choice = self._wait_for_choice(self.opponent, opponent_choices)
            self.opponent_choice = next(s for s in self.opponent_creature.skills 
                                      if s.display_name == opponent_choice.display_name)

            # Resolution phase
            first = self.player
            second = self.opponent
            first_creature = self.player_creature
            second_creature = self.opponent_creature
            first_skill = self.player_choice
            second_skill = self.opponent_choice

            # Speed check
            if second_creature.speed > first_creature.speed or \
               (second_creature.speed == first_creature.speed and random.random() < 0.5):
                first, second = second, first
                first_creature, second_creature = second_creature, first_creature
                first_skill, second_skill = second_skill, first_skill

            # First attack
            damage = self.calculate_damage(first_creature, second_creature, first_skill)
            second_creature.hp -= damage
            self._show_text(self.player, 
                f"{first_creature.display_name} used {first_skill.display_name} for {damage} damage!")

            if second_creature.hp <= 0:
                winner = first
                break

            # Second attack
            damage = self.calculate_damage(second_creature, first_creature, second_skill)
            first_creature.hp -= damage
            self._show_text(self.player,
                f"{second_creature.display_name} used {second_skill.display_name} for {damage} damage!")

            if first_creature.hp <= 0:
                winner = second
                break

        # Show result
        if winner == self.player:
            self._show_text(self.player, "You won!")
        else:
            self._show_text(self.player, "You lost!")

        self._transition_to_scene("MainMenuScene")
