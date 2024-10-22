from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainMenuScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        if not hasattr(self._app, 'all_battles_completed'):
            self._app.all_battles_completed = False

    def __str__(self):
        return "Welcome to Creature Battle!\n1. Play\n2. Quit"

    def run(self):
        self._show_text(self.player, "Welcome to Creature Battle!")
        if self._app.all_battles_completed:
            self._show_text(self.player, "All battles have been completed. Thanks for playing!")
            self._quit_whole_game()
        else:
            choice = self._wait_for_choice(self.player, [
                Button("Play"),
                Button("Quit")
            ])

            if choice.display_name == "Play":
                self._transition_to_scene("MainGameScene")
            else:
                self._quit_whole_game()
