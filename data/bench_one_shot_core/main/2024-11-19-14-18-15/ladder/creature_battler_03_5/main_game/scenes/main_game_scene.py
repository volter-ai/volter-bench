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
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} type)" for skill in self.player_creature.skills])}
"""

    def calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Type effectiveness
        effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "water":
                effectiveness = 0.5
            elif defender.creature_type == "leaf":
                effectiveness = 2.0
        elif skill.skill_type == "water":
            if defender.creature_type == "leaf":
                effectiveness = 0.5
            elif defender.creature_type == "fire":
                effectiveness = 2.0
        elif skill.skill_type == "leaf":
            if defender.creature_type == "fire":
                effectiveness = 0.5
            elif defender.creature_type == "water":
                effectiveness = 2.0

        return int(raw_damage * effectiveness)

    def execute_turn(self):
        # Determine order based on speed
        first = self.player
        second = self.opponent
        first_creature = self.player_creature
        second_creature = self.opponent_creature
        first_skill = self.player_choice
        second_skill = self.opponent_choice

        if self.opponent_creature.speed > self.player_creature.speed or \
           (self.opponent_creature.speed == self.player_creature.speed and random.random() < 0.5):
            first, second = second, first
            first_creature, second_creature = second_creature, first_creature
            first_skill, second_skill = second_skill, first_skill

        # Execute skills
        for attacker, defender, skill, creature, target in [
            (first, second, first_skill, first_creature, second_creature),
            (second, first, second_skill, second_creature, first_creature)
        ]:
            if target.hp > 0:  # Only attack if target still alive
                damage = self.calculate_damage(creature, target, skill)
                target.hp = max(0, target.hp - damage)
                self._show_text(attacker, f"{creature.display_name} used {skill.display_name}! Dealt {damage} damage!")

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player.display_name} vs {self.opponent.display_name}")

        while True:
            # Player choice phase
            skill_buttons = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_buttons)
            self.player_choice = next(s for s in self.player_creature.skills 
                                    if s.display_name == player_choice.display_name)

            # Opponent choice phase
            opponent_choice = self._wait_for_choice(self.opponent, 
                [Button(skill.display_name) for skill in self.opponent_creature.skills])
            self.opponent_choice = next(s for s in self.opponent_creature.skills 
                                      if s.display_name == opponent_choice.display_name)

            # Resolution phase
            self.execute_turn()

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, f"You lost! {self.opponent_creature.display_name} wins!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, f"You won! {self.player_creature.display_name} wins!")
                break

        self._transition_to_scene("MainMenuScene")
