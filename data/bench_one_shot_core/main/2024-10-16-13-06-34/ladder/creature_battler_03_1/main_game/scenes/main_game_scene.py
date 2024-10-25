from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
> Back to Main Menu
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        while True:
            choices = [
                Button("Use Skill"),
                Button("Back to Main Menu")
            ]
            choice = self._wait_for_choice(self.player, choices)

            if choice.display_name == "Use Skill":
                if self.battle_turn():
                    break
            elif choice.display_name == "Back to Main Menu":
                self._transition_to_scene("MainMenuScene")
                return

    def battle_turn(self):
        player_skill = self.player_choose_skill()
        opponent_skill = self.opponent_choose_skill()

        first, second = self.determine_turn_order(
            (self.player_creature, player_skill),
            (self.opponent_creature, opponent_skill)
        )

        for attacker, defender, skill in [first, second]:
            if self.execute_skill(attacker, defender, skill):
                return True
        return False

    def player_choose_skill(self):
        self._show_text(self.player, f"It's your turn! Choose a skill:")
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_choose_skill(self):
        opponent_skill = random.choice(self.opponent_creature.skills)
        self._show_text(self.player, f"{self.opponent_creature.display_name} is preparing to use a skill!")
        return opponent_skill

    def determine_turn_order(self, player_tuple, opponent_tuple):
        player_creature, player_skill = player_tuple
        opponent_creature, opponent_skill = opponent_tuple

        if player_creature.speed > opponent_creature.speed:
            return (player_creature, self.opponent_creature, player_skill), (opponent_creature, self.player_creature, opponent_skill)
        elif player_creature.speed < opponent_creature.speed:
            return (opponent_creature, self.player_creature, opponent_skill), (player_creature, self.opponent_creature, player_skill)
        else:
            if random.choice([True, False]):
                return (player_creature, self.opponent_creature, player_skill), (opponent_creature, self.player_creature, opponent_skill)
            else:
                return (opponent_creature, self.player_creature, opponent_skill), (player_creature, self.opponent_creature, player_skill)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        self._show_text(self.player, f"{attacker.display_name} uses {skill.display_name}!")
        raw_damage = float(attacker.attack) + float(skill.base_damage) - float(defender.defense)
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")
        return self.check_battle_end()

    def calculate_weakness_factor(self, skill_type: str, defender_type: str):
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

    def check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lose!")
            self.end_battle()
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"The opponent's {self.opponent_creature.display_name} fainted! You win!")
            self.end_battle()
            return True
        return False

    def end_battle(self):
        choices = [Button("Back to Main Menu")]
        choice = self._wait_for_choice(self.player, choices)
        self._transition_to_scene("MainMenuScene")
