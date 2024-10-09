from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature
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

Player's turn:
{self.get_skill_choices_str(self.player_creature)}
"""

    def get_skill_choices_str(self, creature: Creature) -> str:
        return "\n".join([f"> {skill.display_name}" for skill in creature.skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self.battle_loop()

    def battle_loop(self):
        while True:
            player_skill = self.player_choice_phase()
            opponent_skill = self.opponent_choice_phase()
            self.resolution_phase(player_skill, opponent_skill)

            if self.check_battle_end():
                break

    def player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def opponent_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def resolution_phase(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self.execute_turn(self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self.execute_turn(self.opponent, self.opponent_creature, opponent_skill, self.player, self.player_creature)
        else:
            # Equal speed, randomly choose who goes first
            if random.choice([True, False]):
                self.execute_turn(self.player, self.player_creature, player_skill, self.opponent, self.opponent_creature)
            else:
                self.execute_turn(self.opponent, self.opponent_creature, opponent_skill, self.player, self.player_creature)

    def execute_turn(self, first_player: Player, first_creature: Creature, first_skill, second_player: Player, second_creature: Creature):
        self.execute_skill(first_player, first_creature, first_skill, second_creature)
        if not self.check_battle_end():
            if first_player == self.player:
                self.execute_skill(second_player, second_creature, self.opponent_choice_phase(), first_creature)
            else:
                self.execute_skill(second_player, second_creature, self.player_choice_phase(), first_creature)

    def execute_skill(self, attacker: Player, attacker_creature: Creature, skill, defender_creature: Creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
