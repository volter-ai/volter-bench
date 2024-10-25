from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainMenuScene(AbstractGameScene):
    def __str__(self):
        return "Welcome to Creature Battle!\n1. Play\n2. Quit"

    def run(self):
        self._show_text(self.player, "Welcome to Creature Battle!")
        choice = self._wait_for_choice(self.player, [
            Button("Play"),
            Button("Quit")
        ])

        if choice.display_name == "Play":
            self._transition_to_scene("MainGameScene")
        elif choice.display_name == "Quit":
            if self.player._listener.__class__.__name__ == "HumanListener" and self.player._listener.random_mode:
                # In random mode, go back to MainGameScene instead of quitting
                self._transition_to_scene("MainGameScene")
            else:
                self._quit_whole_game()
