from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

> Use Skill
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        while True:
            if self.player_turn():
                if self.check_battle_end():
                    break
            if self.opponent_turn():
                if self.check_battle_end():
                    break
        self.end_battle()

    def player_turn(self):
        self._show_text(self.player, f"It's your turn! Choose a skill:")
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return self.execute_skill(self.player_creature, self.opponent_creature, choice.thing)

    def opponent_turn(self):
        opponent_skill = random.choice(self.opponent_creature.skills)
        self._show_text(self.player, f"{self.opponent_creature.display_name} uses {opponent_skill.display_name}!")
        return self.execute_skill(self.opponent_creature, self.player_creature, opponent_skill)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")
        return defender.hp == 0

    def calculate_weakness_factor(self, skill_type: str, defender_type: str):
        if skill_type == defender_type:
            return 1
        elif (skill_type == "fire" and defender_type == "leaf") or \
             (skill_type == "water" and defender_type == "fire") or \
             (skill_type == "leaf" and defender_type == "water"):
            return 2
        elif (skill_type == "fire" and defender_type == "water") or \
             (skill_type == "water" and defender_type == "leaf") or \
             (skill_type == "leaf" and defender_type == "fire"):
            return 0.5
        else:
            return 1

    def check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lost the battle.")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"The opponent's {self.opponent_creature.display_name} fainted! You won the battle!")
            return True
        return False

    def end_battle(self):
        self._show_text(self.player, "The battle has ended. Returning to the main menu.")
        self._transition_to_scene("MainMenuScene")
