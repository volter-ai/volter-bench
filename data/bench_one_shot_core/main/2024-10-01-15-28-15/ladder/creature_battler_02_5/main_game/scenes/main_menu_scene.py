from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainMenuScene(AbstractGameScene):
    def __init__(self, app: "AbstractApp", player: "AbstractPlayer"):
        super().__init__(app, player)
        self.play_count = 0
        self.max_plays = 3  # Maximum number of times to play before quitting

    def __str__(self):
        return "Welcome to Creature Battle!\n1. Play\n2. Quit"

    def run(self):
        while True:
            self._show_text(self.player, "Welcome to Creature Battle!")
            choice = self._wait_for_choice(self.player, [
                Button("Play"),
                Button("Quit")
            ])

            if choice.display_name == "Play":
                self.play_count += 1
                if self.play_count >= self.max_plays:
                    self._show_text(self.player, f"You've played {self.max_plays} times. Time to quit!")
                    self._quit_whole_game()
                    break
                self._transition_to_scene("MainGameScene")
            elif choice.display_name == "Quit":
                self._quit_whole_game()
                break
