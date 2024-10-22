from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainMenuScene(AbstractGameScene):
    MAX_GAMES = 3

    def __init__(self, app: "AbstractApp", player: "AbstractPlayer"):
        super().__init__(app, player)
        self.game_count = 0

    def __str__(self):
        return f"Welcome to Creature Battle!\nGames played: {self.game_count}/{self.MAX_GAMES}\n1. Play\n2. Quit"

    def run(self):
        while self.game_count < self.MAX_GAMES:
            self._show_text(self.player, str(self))
            choice = self._wait_for_choice(self.player, [
                Button("Play"),
                Button("Quit")
            ])

            if choice.display_name == "Play":
                self.game_count += 1
                self._transition_to_scene("MainGameScene")
            elif choice.display_name == "Quit":
                break

        self._show_text(self.player, f"You've played {self.game_count} games. Thanks for playing!")
        self._quit_whole_game()
