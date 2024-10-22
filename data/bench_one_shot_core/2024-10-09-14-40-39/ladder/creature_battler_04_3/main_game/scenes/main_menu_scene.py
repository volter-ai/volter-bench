from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainMenuScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self._reset_creatures()

    def __str__(self):
        return f"""===Main Menu===
Welcome to Creature Battler!

> Play
> Quit
"""

    def run(self):
        while True:
            self._show_text(self.player, str(self))
            play_button = Button("Play")
            quit_button = Button("Quit")
            choices = [play_button, quit_button]
            choice = self._wait_for_choice(self.player, choices)

            if play_button == choice:
                self._transition_to_scene("MainGameScene")
            elif quit_button == choice:
                self._quit_whole_game()

    def _reset_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
