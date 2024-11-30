from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} type)" for skill in self.player_creature.skills])}
"""

    def get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        type_multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_multiplier)

    def execute_turn(self):
        # Determine order based on speed
        first = self.player
        second = self.opponent
        first_creature = self.player_creature
        second_creature = self.opponent_creature
        first_skill = self.player_choice
        second_skill = self.opponent_choice

        if second_creature.speed > first_creature.speed or \
           (second_creature.speed == first_creature.speed and random.random() < 0.5):
            first, second = second, first
            first_creature, second_creature = second_creature, first_creature
            first_skill, second_skill = second_skill, first_skill

        # Execute skills
        for attacker, defender, skill, attacker_creature, defender_creature in [
            (first, second, first_skill, first_creature, second_creature),
            (second, first, second_skill, second_creature, first_creature)
        ]:
            if defender_creature.hp > 0:  # Only execute if defender still alive
                damage = self.calculate_damage(attacker_creature, defender_creature, skill)
                defender_creature.hp = max(0, defender_creature.hp - damage)
                self._show_text(self.player, 
                    f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}! "
                    f"Dealt {damage} damage to {defender.display_name}'s {defender_creature.display_name}!")

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player.display_name} vs {self.opponent.display_name}")

        while True:
            # Player choice phase
            skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            self.player_choice = self._wait_for_choice(self.player, skill_choices).thing

            # Opponent choice phase
            opponent_skill_choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
            self.opponent_choice = self._wait_for_choice(self.opponent, opponent_skill_choices).thing

            # Resolution phase
            self.execute_turn()

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, f"Game Over! {self.opponent.display_name} wins!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, f"Congratulations! {self.player.display_name} wins!")
                break

        self._transition_to_scene("MainMenuScene")
