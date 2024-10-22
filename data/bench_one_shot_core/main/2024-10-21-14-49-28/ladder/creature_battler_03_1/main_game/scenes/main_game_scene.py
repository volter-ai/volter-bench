from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.turn_counter = 0
        self.max_turns = 20  # Set a maximum number of turns for the battle

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
        while True:
            self.turn_counter += 1
            if self.turn_counter > self.max_turns:
                self._show_text(self.player, "The battle has gone on for too long. It's a draw!")
                self._quit_whole_game()
                return

            if self._check_battle_end():
                self._transition_to_scene("MainMenuScene")
                return

            player_skill = self._player_choose_skill()
            opponent_skill = self._opponent_choose_skill()

            first, second = self._determine_turn_order(
                (self.player_creature, player_skill),
                (self.opponent_creature, opponent_skill)
            )

            self._execute_turn(first[0], first[1], second[0])
            if self._check_battle_end():
                self._transition_to_scene("MainMenuScene")
                return

            self._execute_turn(second[0], second[1], first[0])
            if self._check_battle_end():
                self._transition_to_scene("MainMenuScene")
                return

    def _player_choose_skill(self) -> Skill:
        self._show_text(self.player, "Your turn!")
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _opponent_choose_skill(self) -> Skill:
        return random.choice(self.opponent_creature.skills)

    def _determine_turn_order(self, player_tuple, opponent_tuple):
        player_creature, player_skill = player_tuple
        opponent_creature, opponent_skill = opponent_tuple

        if player_creature.speed > opponent_creature.speed:
            return player_tuple, opponent_tuple
        elif player_creature.speed < opponent_creature.speed:
            return opponent_tuple, player_tuple
        else:
            # If speeds are equal, randomly decide who goes first
            return random.choice([(player_tuple, opponent_tuple), (opponent_tuple, player_tuple)])

    def _execute_turn(self, attacker: Creature, skill: Skill, defender: Creature):
        self._show_text(self.player, f"{attacker.display_name}'s turn!")
        self._execute_skill(attacker, defender, skill)

    def _execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        defender.hp = max(0, defender.hp - final_damage)

        self._show_text(self.player, f"{attacker.display_name} uses {skill.display_name}!")
        self._show_text(self.player, f"It deals {final_damage} damage to {defender.display_name}!")

    def _get_type_factor(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
        elif skill_type == "fire" and defender_type == "leaf":
            return 2.0
        elif skill_type == "water" and defender_type == "fire":
            return 2.0
        elif skill_type == "leaf" and defender_type == "water":
            return 2.0
        elif skill_type == "fire" and defender_type == "water":
            return 0.5
        elif skill_type == "water" and defender_type == "leaf":
            return 0.5
        elif skill_type == "leaf" and defender_type == "fire":
            return 0.5
        else:
            return 1.0

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent_creature.display_name} fainted! You win!")
            return True
        return False
