from mini_game_engine.engine.lib import AbstractGameScene, Button, RandomModeGracefulExit


class MainMenuScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)

    def __str__(self):
        return "Welcome to Creature Battle!\n1. Play\n2. Quit"

    def run(self):
        self._show_text(self.player, "Welcome to Creature Battle!")
        try:
            choice = self._wait_for_choice(self.player, [
                Button("Play"),
                Button("Quit")
            ])

            if choice.display_name == "Play":
                self._transition_to_scene("MainGameScene")
            elif choice.display_name == "Quit":
                self._quit_whole_game()
        except RandomModeGracefulExit:
            self._quit_whole_game()
