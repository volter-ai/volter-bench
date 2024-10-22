from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainMenuScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.game_count = 0
        self.max_games = 3  # Limit the number of games

    def __str__(self):
        return f"""===Main Menu===
Welcome to Creature Battler!
Games played: {self.game_count}/{self.max_games}

> Play
> Quit
"""

    def run(self):
        self.game_loop()

    def game_loop(self):
        while self.game_count < self.max_games:
            play_button = Button("Play")
            quit_button = Button("Quit")
            choices = [play_button, quit_button]
            choice = self._wait_for_choice(self.player, choices)

            if play_button == choice:
                self.game_count += 1
                self._transition_to_scene("MainGameScene")
            elif quit_button == choice:
                self._quit_whole_game()

        self._show_text(self.player, "Maximum number of games reached. Thanks for playing!")
        self._quit_whole_game()
