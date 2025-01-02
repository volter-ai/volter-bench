from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        return f"""=== Main Game Scene ===
Player: {self.player.display_name}
Opponent: {self.opponent.display_name}
"""

    def run(self):
        while True:
            player_choice = self._player_choice_phase()
            opponent_choice = self._foe_choice_phase()
            self._resolution_phase(player_choice, opponent_choice)

    def _player_choice_phase(self):
        skills = self.player.creatures[0].skills
        choices = [SelectThing(skill) for skill in skills]
        return self._wait_for_choice(self.player, choices)

    def _foe_choice_phase(self):
        skills = self.opponent.creatures[0].skills
        choices = [SelectThing(skill) for skill in skills]
        return self._wait_for_choice(self.opponent, choices)

    def _resolution_phase(self, player_choice, opponent_choice):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        # Determine order based on speed
        if player_creature.speed > opponent_creature.speed:
            self._execute_skill(player_creature, opponent_creature, player_choice.thing)
            if opponent_creature.hp > 0:
                self._execute_skill(opponent_creature, player_creature, opponent_choice.thing)
        elif opponent_creature.speed > player_creature.speed:
            self._execute_skill(opponent_creature, player_creature, opponent_choice.thing)
            if player_creature.hp > 0:
                self._execute_skill(player_creature, opponent_creature, player_choice.thing)
        else:
            # Randomly decide who goes first if speeds are equal
            if random.choice([True, False]):
                self._execute_skill(player_creature, opponent_creature, player_choice.thing)
                if opponent_creature.hp > 0:
                    self._execute_skill(opponent_creature, player_creature, opponent_choice.thing)
            else:
                self._execute_skill(opponent_creature, player_creature, opponent_choice.thing)
                if player_creature.hp > 0:
                    self._execute_skill(player_creature, opponent_creature, player_choice.thing)

        # Check for battle end conditions
        if player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._quit_whole_game()
        elif opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._quit_whole_game()

    def _execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        final_damage = self._calculate_final_damage(skill.skill_type, defender.creature_type, raw_damage)
        defender.hp = max(0, defender.hp - int(final_damage))

    def _calculate_final_damage(self, skill_type: str, creature_type: str, raw_damage: float) -> float:
        type_effectiveness = {
            "normal": {"normal": 1, "fire": 1, "water": 1, "leaf": 1},
            "fire": {"normal": 1, "fire": 0.5, "water": 0.5, "leaf": 2},
            "water": {"normal": 1, "fire": 2, "water": 0.5, "leaf": 0.5},
            "leaf": {"normal": 1, "fire": 0.5, "water": 2, "leaf": 0.5}
        }
        effectiveness = type_effectiveness[skill_type][creature_type]
        return raw_damage * effectiveness
