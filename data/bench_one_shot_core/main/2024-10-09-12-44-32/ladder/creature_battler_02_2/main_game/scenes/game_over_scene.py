from mini_game_engine.engine.lib import AbstractGameScene, Button


class GameOverScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)

    def __str__(self):
        return """===Game Over===
What would you like to do?
> New Game
> Quit
"""

    def run(self):
        self._show_text(self.player, "Game Over! Thanks for playing!")
        self.game_over_loop()

    def game_over_loop(self):
        while True:
            new_game_button = Button("New Game")
            quit_button = Button("Quit")
            choices = [new_game_button, quit_button]
            choice = self._wait_for_choice(self.player, choices)

            if new_game_button == choice:
                self._transition_to_scene("MainMenuScene")
                self._quit_whole_game()  # End the current game session after starting a new game
            elif quit_button == choice:
                self._quit_whole_game()
            else:
                self._show_text(self.player, "Invalid choice. Please try again.")
