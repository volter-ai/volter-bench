from mini_game_engine.engine.lib import (AbstractGameScene, Button,
                                         HumanListener)


class MainMenuScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)

    def __str__(self):
        return """===Main Menu===
Welcome to Creature Battler

> Play
> Quit
"""

    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            play_button = Button("Play")
            quit_button = Button("Quit")
            choices = [play_button, quit_button]
            choice = self._wait_for_choice(self.player, choices)

            if play_button == choice:
                self._transition_to_scene("MainGameScene")
            elif quit_button == choice:
                self._quit_whole_game()

            # Check if we're in random mode and have reached the end of our random moves
            if isinstance(self.player._listener, HumanListener) and self.player._listener.random_mode:
                if self.player._listener.random_mode_counter <= 0:
                    self._quit_whole_game()
