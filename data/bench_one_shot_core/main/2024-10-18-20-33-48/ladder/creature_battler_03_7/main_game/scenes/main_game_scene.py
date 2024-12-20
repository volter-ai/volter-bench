from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Available skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, "A wild opponent appears!")
        while True:
            if self._is_battle_over():
                self._handle_battle_end()
                break
            self._execute_turn()

    def _execute_turn(self):
        player_skill = self._get_player_skill()
        opponent_skill = self._get_opponent_skill()

        first, second = self._determine_turn_order(
            (self.player_creature, player_skill),
            (self.opponent_creature, opponent_skill)
        )

        self._execute_skill(*first)
        if not self._is_battle_over():
            self._execute_skill(*second)

    def _get_player_skill(self):
        self._show_text(self.player, "Your turn to choose a skill!")
        skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, skill_choices)
        return choice.thing

    def _get_opponent_skill(self):
        self._show_text(self.player, f"{self.opponent.display_name}'s turn to choose a skill!")
        skill_choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, skill_choices)
        return choice.thing

    def _determine_turn_order(self, player_tuple, opponent_tuple):
        player_creature, player_skill = player_tuple
        opponent_creature, opponent_skill = opponent_tuple

        if player_creature.speed > opponent_creature.speed:
            return player_tuple, opponent_tuple
        elif player_creature.speed < opponent_creature.speed:
            return opponent_tuple, player_tuple
        else:
            return random.sample([player_tuple, opponent_tuple], 2)

    def _execute_skill(self, attacker: Creature, skill: Skill):
        defender = self.opponent_creature if attacker == self.player_creature else self.player_creature
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        defender.hp = max(0, defender.hp - final_damage)

        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")

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

    def _is_battle_over(self) -> bool:
        return self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0

    def _handle_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")
        
        self._show_text(self.player, "Returning to main menu...")
        self._transition_to_scene("MainMenuScene")
