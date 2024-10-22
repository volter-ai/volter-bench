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
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        while True:
            self._reset_battle()
            self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
            while True:
                if self._check_battle_end():
                    break
                self._execute_battle_round()
                if self._check_battle_end():
                    break
            
            if not self._play_again():
                break

    def _reset_battle(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def _determine_turn_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player_creature, self.player, self.opponent_creature, self.opponent)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent_creature, self.opponent, self.player_creature, self.player)
        else:
            creatures = [self.player_creature, self.opponent_creature]
            players = [self.player, self.opponent]
            first = random.choice([0, 1])
            second = 1 - first
            return (creatures[first], players[first], creatures[second], players[second])

    def _execute_battle_round(self):
        first_creature, first_player, second_creature, second_player = self._determine_turn_order()
        
        self._execute_turn(first_creature, first_player, second_creature)
        if not self._check_battle_end():
            self._execute_turn(second_creature, second_player, first_creature)

    def _execute_turn(self, attacker: Creature, attacker_player: Player, defender: Creature):
        self._show_text(self.player, f"{attacker_player.display_name}'s turn!")
        if attacker_player == self.player:
            choices = [SelectThing(skill, label=skill.display_name) for skill in attacker.skills]
            choice = self._wait_for_choice(attacker_player, choices)
            skill = choice.thing
        else:
            skill = random.choice(attacker.skills)
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

    def _play_again(self) -> bool:
        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choices = [play_again_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if choice == play_again_button:
            return True
        elif choice == quit_button:
            self._transition_to_scene("MainMenuScene")
            return False
