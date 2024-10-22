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
        return "\n".join([f"> {skill.display_name} ({skill.skill_type} type, {skill.base_damage} damage)" for skill in skills])

    def run(self):
        while True:
            self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
            self._reset_creatures()
            
            while True:
                if self._check_battle_end():
                    break
                player_skill = self._player_choice()
                opponent_skill = self._opponent_choice()
                self._resolve_skills(player_skill, opponent_skill)
                if self._check_battle_end():
                    break
            
            play_again = self._ask_play_again()
            if not play_again:
                self._quit_whole_game()
                return

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def _player_choice(self) -> Skill:
        self._show_text(self.player, "Your turn!")
        choices = [SelectThing(skill, label=f"{skill.display_name} ({skill.skill_type} type)") for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _opponent_choice(self) -> Skill:
        self._show_text(self.player, f"{self.opponent.display_name}'s turn!")
        return random.choice(self.opponent_creature.skills)

    def _resolve_skills(self, player_skill: Skill, opponent_skill: Skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            first_attacker, first_skill = self.player_creature, player_skill
            second_attacker, second_skill = self.opponent_creature, opponent_skill
        elif self.player_creature.speed < self.opponent_creature.speed:
            first_attacker, first_skill = self.opponent_creature, opponent_skill
            second_attacker, second_skill = self.player_creature, player_skill
        else:
            if random.choice([True, False]):
                first_attacker, first_skill = self.player_creature, player_skill
                second_attacker, second_skill = self.opponent_creature, opponent_skill
            else:
                first_attacker, first_skill = self.opponent_creature, opponent_skill
                second_attacker, second_skill = self.player_creature, player_skill

        self._execute_skill(first_attacker, second_attacker, first_skill)
        if second_attacker.hp > 0:
            self._execute_skill(second_attacker, first_attacker, second_skill)

    def _execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        self._show_text(self.player, f"{attacker.display_name} uses {skill.display_name}!")
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{defender.display_name} takes {final_damage} damage!")

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

    def _ask_play_again(self) -> bool:
        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choices = [play_again_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)
        return choice == play_again_button
