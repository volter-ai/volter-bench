from main_game.models import Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app: "AbstractApp", player: Player):
        super().__init__(app, player)
        self.bot = app.create_bot("default_player")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.turn_count = 0
        self.max_turns = 10  # Limit the number of turns for testing purposes

    def __str__(self):
        return (
            f"Player: {self.player.display_name}\n"
            f"Creature: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})\n"
            f"Bot: {self.bot.display_name}\n"
            f"Creature: {self.bot_creature.display_name} (HP: {self.bot_creature.hp}/{self.bot_creature.max_hp})"
        )

    def run(self):
        while self.turn_count < self.max_turns:
            self._show_text(self.player, str(self))
            self._show_text(self.bot, str(self))

            player_skill = self._player_choice_phase()
            bot_skill = self._bot_choice_phase()

            self._resolution_phase(player_skill, bot_skill)

            if self._check_battle_end():
                break

            self.turn_count += 1

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _player_choice_phase(self) -> Skill:
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _bot_choice_phase(self) -> Skill:
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        return choice.thing

    def _resolution_phase(self, player_skill: Skill, bot_skill: Skill):
        self.bot_creature.hp -= player_skill.damage
        self.player_creature.hp -= bot_skill.damage

        self._show_text(self.player, f"You used {player_skill.display_name} and dealt {player_skill.damage} damage!")
        self._show_text(self.bot, f"Bot used {bot_skill.display_name} and dealt {bot_skill.damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.bot, "You won the battle!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.bot, "You lost the battle!")
            return True
        return False

    def _reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
