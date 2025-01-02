from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        return f"""=== Main Game ===
Player: {self.player.display_name}
Opponent: {self.opponent.display_name}

Your Creatures:
{self._creature_status(self.player.creatures)}

Opponent's Creatures:
{self._creature_status(self.opponent.creatures)}
"""

    def _creature_status(self, creatures):
        return "\n".join([f"{creature.display_name} - HP: {creature.hp}/{creature.max_hp}" for creature in creatures])

    def run(self):
        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()
            if self.check_battle_end():
                break

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

        # Determine turn order
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
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        final_damage = self.calculate_final_damage(skill.skill_type, defender.creature_type, raw_damage)
        defender.hp = max(defender.hp - int(final_damage), 0)

    def calculate_final_damage(self, skill_type: str, creature_type: str, raw_damage: float) -> float:
        effectiveness = self.get_effectiveness(skill_type, creature_type)
        return effectiveness * raw_damage

    def get_effectiveness(self, skill_type: str, creature_type: str) -> float:
        effectiveness_chart = {
            "normal": {},
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)

    def check_battle_end(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]
        if player_creature.hp <= 0 or opponent_creature.hp <= 0:
            winner = "Player" if opponent_creature.hp <= 0 else "Opponent"
            self._show_text(self.player, f"{winner} wins!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
