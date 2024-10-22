from mini_game_engine.engine.lib import AbstractGameScene, Button


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
        while True:
            play_button = Button("Play")
            quit_button = Button("Quit")
            choices = [play_button, quit_button]
            choice = self._wait_for_choice(self.player, choices)

            if play_button == choice:
                self._transition_to_scene("MainGameScene")
            elif quit_button == choice:
                self._quit_whole_game()

            # After returning from MainGameScene, ask if the player wants to play again
            play_again_button = Button("Play Again")
            quit_button = Button("Quit")
            choices = [play_again_button, quit_button]
            self._show_text(self.player, "Do you want to play again?")
            choice = self._wait_for_choice(self.player, choices)

            if play_again_button == choice:
                self._transition_to_scene("MainGameScene")
            elif quit_button == choice:
                self._quit_whole_game()
