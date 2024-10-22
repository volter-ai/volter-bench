from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainMenuScene(AbstractGameScene):
    def __init__(self, app: "AbstractApp", player: "AbstractPlayer"):
        super().__init__(app, player)
        self.games_played = 0
        self.max_games = 3  # Set a maximum number of games to play

    def __str__(self):
        return "Welcome to Creature Battle!\n1. Play\n2. Quit"

    def run(self):
        self._show_text(self.player, "Welcome to Creature Battle!")
        
        while self.games_played < self.max_games:
            choice = self._wait_for_choice(self.player, [
                Button("Play"),
                Button("Quit")
            ])

            if choice.display_name == "Play":
                self.games_played += 1
                self._transition_to_scene("MainGameScene")
            elif choice.display_name == "Quit":
                break

        self._quit_whole_game()
