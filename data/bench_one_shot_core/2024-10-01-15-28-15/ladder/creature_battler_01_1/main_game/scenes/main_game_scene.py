from collections import deque

from main_game.models import Creature, Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainGameScene(AbstractGameScene):
    def __init__(self, app: "AbstractApp", player: Player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.skill_queue = deque()

    def __str__(self):
        return (
            f"Player: {self.player.display_name} - {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})\n"
            f"Opponent: {self.opponent.display_name} - {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})\n"
            "Available skills:\n" + "\n".join([f"- {skill.display_name}" for skill in self.player_creature.skills])
        )

    def run(self):
        while True:
            self._show_text(self.player, str(self))
            self._show_text(self.opponent, str(self))

            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)
            self.skill_queue.append((self.player, self.player_creature, player_skill))

            # Foe Choice Phase
            opponent_skill = self._player_choice_phase(self.opponent, self.opponent_creature)
            self.skill_queue.append((self.opponent, self.opponent_creature, opponent_skill))

            # Resolution Phase
            self._resolution_phase()

            if self._check_battle_end():
                break

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self, current_player: Player, current_creature: Creature) -> Skill:
        choices = [Button(skill.display_name) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return next(skill for skill in current_creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self):
        while self.skill_queue:
            self._execute_skills()

    def _execute_skills(self):
        attacker, attacker_creature, skill = self.skill_queue.popleft()
        if attacker == self.player:
            defender = self.opponent
            defender_creature = self.opponent_creature
        else:
            defender = self.player
            defender_creature = self.player_creature

        defender_creature.hp -= skill.damage
        self._show_text(attacker, f"Your {attacker_creature.display_name} used {skill.display_name} and dealt {skill.damage} damage!")
        self._show_text(defender, f"Opponent's {attacker_creature.display_name} used {skill.display_name} and dealt {skill.damage} damage!")

    def _check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
