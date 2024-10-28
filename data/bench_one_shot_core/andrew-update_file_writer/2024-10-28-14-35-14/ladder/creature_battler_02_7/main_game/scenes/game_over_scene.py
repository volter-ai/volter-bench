from mini_game_engine.engine.lib import AbstractGameScene, Button


class GameOverScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.winner = None

    def __str__(self):
        return f"""===Game Over===
{self.winner.display_name} has won the battle!

> Play Again
> Quit
"""

    def run(self):
        previous_scene = self._app._scene_stack[-2]
        self.winner = previous_scene.winner

        self._show_text(self.player, f"{self.winner.display_name} has won the battle!")

        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choices = [play_again_button, quit_button]

        choice = self._wait_for_choice(self.player, choices)

        if choice == play_again_button:
            self._transition_to_scene("MainGameScene")
        elif choice == quit_button:
            self._quit_whole_game()
