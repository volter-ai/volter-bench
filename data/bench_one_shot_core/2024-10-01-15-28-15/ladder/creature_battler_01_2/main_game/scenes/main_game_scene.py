from typing import List

from main_game.models import Creature, Player, Skill
from mini_game_engine.engine.lib import (AbstractGameScene, AbstractPlayer,
                                         Button)


class MainGameScene(AbstractGameScene):
    def __init__(self, app: "AbstractApp", player: Player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.players = [self.player, self.opponent]
        self.creatures = [player.creatures[0] for player in self.players]
        self.skill_queue: List[Skill] = []

    def __str__(self):
        return "\n".join([
            f"{player.display_name}: {creature.display_name} (HP: {creature.hp}/{creature.max_hp})"
            for player, creature in zip(self.players, self.creatures)
        ] + ["Available skills:"] + [
            f"- {skill.display_name}" for skill in self.creatures[0].skills
        ])

    def run(self):
        while True:
            for player in self.players:
                self._show_text(player, str(self))

            # Choice Phase
            for player, creature in zip(self.players, self.creatures):
                self._player_choice_phase(player, creature)

            # Resolution Phase
            self._resolution_phase()

            if self._check_battle_end():
                break

        self._reset_and_transition()

    def _player_choice_phase(self, current_player: AbstractPlayer, current_creature: Creature):
        choices = [Button(skill.display_name) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        chosen_skill = next(skill for skill in current_creature.skills if skill.display_name == choice.display_name)
        self.skill_queue.append(chosen_skill)

    def _resolution_phase(self):
        for i, skill in enumerate(self.skill_queue):
            attacker = self.players[i]
            defender = self.players[1 - i]
            attacker_creature = self.creatures[i]
            defender_creature = self.creatures[1 - i]

            defender_creature.hp -= skill.damage
            for player in self.players:
                self._show_text(player, f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name} and dealt {skill.damage} damage!")

        self.skill_queue.clear()

    def _check_battle_end(self) -> bool:
        for i, creature in enumerate(self.creatures):
            if creature.hp <= 0:
                winner = self.players[1 - i]
                loser = self.players[i]
                for player in self.players:
                    self._show_text(player, f"{winner.display_name} won the battle!")
                return True
        return False

    def _reset_creatures(self):
        for creature in self.creatures:
            creature.hp = creature.max_hp

    def _reset_and_transition(self):
        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")
