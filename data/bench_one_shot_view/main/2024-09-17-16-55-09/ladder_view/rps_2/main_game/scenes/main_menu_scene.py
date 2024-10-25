from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainMenuScene(AbstractGameScene):
    def run(self):
        self._show_text(self.player, "Welcome to Rock Paper Scissors!")
        choice = self._wait_for_choice(self.player, [
            Button("Play"),
            Button("Quit")
        ])

        if choice.display_name == "Play":
            self._transition_to_scene("MainGameScene")
        else:
            self._quit_whole_game()

    def __str__(self):
        return "Main Menu: Choose to Play or Quit"
