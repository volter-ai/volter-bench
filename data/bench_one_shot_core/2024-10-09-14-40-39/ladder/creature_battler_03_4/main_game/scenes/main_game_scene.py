from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

> Use Skill
> Quit
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self.game_loop()

    def game_loop(self):
        while True:
            use_skill_button = Button("Use Skill")
            quit_button = Button("Quit")
            choices = [use_skill_button, quit_button]
            choice = self._wait_for_choice(self.player, choices)

            if use_skill_button == choice:
                self.battle_turn()
            elif quit_button == choice:
                self._quit_whole_game()

            if self.check_battle_end():
                break

        self._transition_to_scene("MainMenuScene")

    def battle_turn(self):
        player_skill = self.choose_skill(self.player, self.player_creature)
        opponent_skill = self.choose_skill(self.opponent, self.opponent_creature)

        first, second = self.determine_turn_order(
            (self.player, self.player_creature, player_skill),
            (self.opponent, self.opponent_creature, opponent_skill)
        )

        self.execute_skill(*first)
        if not self.check_battle_end():
            self.execute_skill(*second)

    def choose_skill(self, player: Player, creature: Creature) -> Skill:
        skill_choices = [SelectThing(skill) for skill in creature.skills]
        choice = self._wait_for_choice(player, skill_choices)
        return choice.thing

    def determine_turn_order(self, pair1, pair2):
        if pair1[1].speed > pair2[1].speed:
            return pair1, pair2
        elif pair1[1].speed < pair2[1].speed:
            return pair2, pair1
        else:
            return random.sample([pair1, pair2], 2)

    def execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill):
        defender = self.opponent if attacker == self.player else self.player
        defender_creature = self.opponent_creature if attacker == self.player else self.player_creature

        raw_damage = float(attacker_creature.attack + skill.base_damage - defender_creature.defense)
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)

        defender_creature.hp = max(0, defender_creature.hp - final_damage)

        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} took {final_damage} damage!")

    def calculate_weakness_factor(self, skill_type: str, defender_type: str) -> float:
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

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            return True
        return False
