from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]
        return f"""=== Main Game ===
Player: {self.player.display_name}
Creature: {player_creature.display_name} (HP: {player_creature.hp}/{player_creature.max_hp})

Opponent: {self.opponent.display_name}
Creature: {opponent_creature.display_name} (HP: {opponent_creature.hp}/{opponent_creature.max_hp})

Choose a skill:
"""

    def run(self):
        while self.player.creatures[0].hp > 0 and self.opponent.creatures[0].hp > 0:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()

        self.end_battle()

    def player_choice_phase(self):
        player_creature = self.player.creatures[0]
        choices = [SelectThing(skill) for skill in player_creature.skills]
        self.player_choice = self._wait_for_choice(self.player, choices)

    def foe_choice_phase(self):
        opponent_creature = self.opponent.creatures[0]
        choices = [SelectThing(skill) for skill in opponent_creature.skills]
        self.foe_choice = self._wait_for_choice(self.opponent, choices)

    def resolution_phase(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        # Determine the order of execution based on speed
        if player_creature.speed > opponent_creature.speed:
            self.execute_skill(player_creature, opponent_creature, self.player_choice.thing)
            if opponent_creature.hp > 0:
                self.execute_skill(opponent_creature, player_creature, self.foe_choice.thing)
        elif opponent_creature.speed > player_creature.speed:
            self.execute_skill(opponent_creature, player_creature, self.foe_choice.thing)
            if player_creature.hp > 0:
                self.execute_skill(player_creature, opponent_creature, self.player_choice.thing)
        else:
            # Randomly decide who goes first if speeds are equal
            if random.choice([True, False]):
                self.execute_skill(player_creature, opponent_creature, self.player_choice.thing)
                if opponent_creature.hp > 0:
                    self.execute_skill(opponent_creature, player_creature, self.foe_choice.thing)
            else:
                self.execute_skill(opponent_creature, player_creature, self.foe_choice.thing)
                if player_creature.hp > 0:
                    self.execute_skill(player_creature, opponent_creature, self.player_choice.thing)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply weakness-resistance factor
        factor = self.get_weakness_resistance_factor(skill.skill_type, defender.creature_type)
        final_damage = int(factor * raw_damage)

        # Subtract damage from defender's hp
        defender.hp = max(0, defender.hp - final_damage)

    def get_weakness_resistance_factor(self, skill_type: str, creature_type: str) -> float:
        # Define type relationships
        effectiveness = {
            "normal": {},
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)

    def end_battle(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]
        if player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
        elif opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")

        # Reset creatures' state
        player_creature.hp = player_creature.max_hp
        opponent_creature.hp = opponent_creature.max_hp

        self._transition_to_scene("MainMenuScene")
