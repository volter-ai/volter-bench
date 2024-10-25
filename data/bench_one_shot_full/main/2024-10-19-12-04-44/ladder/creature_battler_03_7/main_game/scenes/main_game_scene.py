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
            player_skill = self._player_turn()
            opponent_skill = self._opponent_turn()
            self._resolution_phase(player_skill, opponent_skill)

    def _player_turn(self):
        self._show_text(self.player, "Your turn!")
        skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, skill_choices)
        return choice.thing

    def _opponent_turn(self):
        self._show_text(self.player, f"{self.opponent.display_name}'s turn!")
        skill_choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, skill_choices)
        return choice.thing

    def _resolution_phase(self, player_skill: Skill, opponent_skill: Skill):
        first, second = self._determine_skill_order(
            (self.player_creature, player_skill),
            (self.opponent_creature, opponent_skill)
        )

        self._execute_skill(*first)
        if not self._is_battle_over():
            self._execute_skill(*second)

    def _determine_skill_order(self, pair1: tuple[Creature, Skill], pair2: tuple[Creature, Skill]):
        creature1, skill1 = pair1
        creature2, skill2 = pair2

        if creature1.speed > creature2.speed:
            return pair1, pair2
        elif creature2.speed > creature1.speed:
            return pair2, pair1
        else:
            return random.sample([pair1, pair2], 2)

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
