from main_game.models import Creature, Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainGameScene(AbstractGameScene):
    def __init__(self, app: "AbstractApp", player: Player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

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

            # Foe Choice Phase
            opponent_skill = self._player_choice_phase(self.opponent, self.opponent_creature)

            # Resolution Phase
            self._resolution_phase(player_skill, opponent_skill)

            if self._check_battle_end():
                break

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self, current_player: Player, current_creature: Creature) -> Skill:
        choices = [Button(skill.display_name) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return next(skill for skill in current_creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill: Skill, opponent_skill: Skill):
        self.opponent_creature.hp -= player_skill.damage
        self._show_text(self.player, f"Your {self.player_creature.display_name} used {player_skill.display_name} and dealt {player_skill.damage} damage!")
        self._show_text(self.opponent, f"Opponent's {self.player_creature.display_name} used {player_skill.display_name} and dealt {player_skill.damage} damage!")

        if self.opponent_creature.hp > 0:
            self.player_creature.hp -= opponent_skill.damage
            self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} used {opponent_skill.display_name} and dealt {opponent_skill.damage} damage!")
            self._show_text(self.opponent, f"Your {self.opponent_creature.display_name} used {opponent_skill.display_name} and dealt {opponent_skill.damage} damage!")

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
