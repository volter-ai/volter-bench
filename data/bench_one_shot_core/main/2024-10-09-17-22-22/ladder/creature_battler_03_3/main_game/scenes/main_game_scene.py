from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        # Initialize with default skills
        self.player_skill = self.player_creature.skills[0]
        self.opponent_skill = self.opponent_creature.skills[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

> Use Skill
> Quit
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        while True:
            if self.player_creature.hp <= 0:
                self.end_battle("You lost the battle!")
                break
            if self.opponent_creature.hp <= 0:
                self.end_battle("You won the battle!")
                break

            self.player_turn()
            self.opponent_turn()
            self.resolution_phase()

    def player_turn(self):
        use_skill_button = Button("Use Skill")
        quit_button = Button("Quit")
        choices = [use_skill_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if use_skill_button == choice:
            skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            skill_choice = self._wait_for_choice(self.player, skill_choices)
            self.player_skill = skill_choice.thing
        elif quit_button == choice:
            self._quit_whole_game()
        # If we reach here, it means the player didn't quit, so we ensure a skill is set
        if self.player_skill is None:
            self.player_skill = random.choice(self.player_creature.skills)

    def opponent_turn(self):
        self.opponent_skill = random.choice(self.opponent_creature.skills)

    def resolution_phase(self):
        # Ensure both skills are set before proceeding
        if self.player_skill is None or self.opponent_skill is None:
            raise ValueError("Both player and opponent must have a skill selected before resolution phase")

        first, second = self.determine_execution_order(
            (self.player_creature, self.player_skill),
            (self.opponent_creature, self.opponent_skill)
        )
        self.execute_skill(*first)
        if second[0].hp > 0:  # Check if the second creature is still alive
            self.execute_skill(*second)

        # Reset skills for the next turn
        self.player_skill = None
        self.opponent_skill = None

    def determine_execution_order(self, pair1, pair2):
        creature1, skill1 = pair1
        creature2, skill2 = pair2
        if creature1.speed > creature2.speed:
            return pair1, pair2
        elif creature2.speed > creature1.speed:
            return pair2, pair1
        else:
            return random.choice([(pair1, pair2), (pair2, pair1)])

    def execute_skill(self, attacker: Creature, skill: Skill):
        defender = self.opponent_creature if attacker == self.player_creature else self.player_creature
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender.hp = max(0, defender.hp - final_damage)

        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")

    @staticmethod
    def calculate_weakness_factor(skill_type: str, defender_type: str) -> float:
        if skill_type == defender_type:
            return 1.0
        elif (skill_type == "fire" and defender_type == "leaf") or \
             (skill_type == "water" and defender_type == "fire") or \
             (skill_type == "leaf" and defender_type == "water"):
            return 2.0
        elif (skill_type == "fire" and defender_type == "water") or \
             (skill_type == "water" and defender_type == "leaf") or \
             (skill_type == "leaf" and defender_type == "fire"):
            return 0.5
        else:
            return 1.0

    def end_battle(self, message: str):
        self._show_text(self.player, message)
        self._transition_to_scene("MainMenuScene")
