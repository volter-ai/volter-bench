from mini_game_engine.engine.lib import AbstractGameScene, Button, AbstractApp
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app: AbstractApp, player: Player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.turn_counter = 0
        self.max_turns = 10
        self._reset_creatures()

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def __str__(self):
        return (
            f"Player: {self.player.display_name}\n"
            f"Creature: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})\n"
            f"Opponent: {self.opponent.display_name}\n"
            f"Creature: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})\n"
            f"Available skills:\n" + "\n".join([f"- {skill.display_name}" for skill in self.player_creature.skills])
        )

    def run(self):
        while self.turn_counter < self.max_turns:
            self.turn_counter += 1
            self._show_text(self.player, str(self))
            self._show_text(self.opponent, str(self))

            player_skill = self._player_choice_phase()
            opponent_skill = self._foe_choice_phase()

            self._resolution_phase(player_skill, opponent_skill)

            if self._check_battle_end():
                return

        self._show_text(self.player, "The battle has reached the maximum number of turns. It's a draw!")
        self._show_text(self.opponent, "The battle has reached the maximum number of turns. It's a draw!")
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self) -> Skill:
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _foe_choice_phase(self) -> Skill:
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill: Skill, opponent_skill: Skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self._execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
            if not self._check_battle_end():
                self._execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self._execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
            if not self._check_battle_end():
                self._execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
        else:
            if random.choice([True, False]):
                self._execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
                if not self._check_battle_end():
                    self._execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
            else:
                self._execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
                if not self._check_battle_end():
                    self._execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)

    def _execute_skill(self, attacker: Player, attacker_creature: Creature, skill: Skill, defender_creature: Creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender_creature.display_name}!")
        self._show_text(self.opponent, f"{attacker_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender_creature.display_name}!")

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
