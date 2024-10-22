from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
        while True:
            if self._check_battle_end():
                self._show_battle_result()
                self._return_to_main_menu()
                break
            
            first, second = self._determine_turn_order()
            self._execute_turn(first)
            
            if self._check_battle_end():
                self._show_battle_result()
                self._return_to_main_menu()
                break
            
            self._execute_turn(second)

    def _determine_turn_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return self.player, self.opponent
        elif self.player_creature.speed < self.opponent_creature.speed:
            return self.opponent, self.player
        else:
            # If speeds are equal, randomly choose who goes first
            return random.sample([self.player, self.opponent], 2)

    def _execute_turn(self, acting_player):
        if acting_player == self.player:
            self._player_turn()
        else:
            self._opponent_turn()

    def _player_turn(self):
        self._show_text(self.player, "Your turn!")
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self._execute_skill(self.player_creature, self.opponent_creature, choice.thing)

    def _opponent_turn(self):
        self._show_text(self.player, f"{self.opponent.display_name}'s turn!")
        skill = random.choice(self.opponent_creature.skills)
        self._execute_skill(self.opponent_creature, self.player_creature, skill)

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
        return self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0

    def _show_battle_result(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lose!")
        else:
            self._show_text(self.player, f"{self.opponent_creature.display_name} fainted! You win!")

    def _return_to_main_menu(self):
        return_button = Button("Return to Main Menu")
        choice = self._wait_for_choice(self.player, [return_button])
        if choice == return_button:
            self._transition_to_scene("MainMenuScene")
