from mini_game_engine.engine.lib import AbstractGameScene, Button


class BattleResultScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.winner = None

    def __str__(self):
        result = "You win!" if self.winner == self.player else "You lose!"
        return f"""===Battle Result===
{result}

> Return to Main Menu
> Quit Game
"""

    def run(self):
        # Retrieve the winner from the MainGameScene
        main_game_scene = self._app.scene_registry["MainGameScene"](self._app, self.player)
        self.winner = main_game_scene.winner
        self.game_loop()

    def game_loop(self):
        while True:
            return_button = Button("Return to Main Menu")
            quit_button = Button("Quit Game")
            choices = [return_button, quit_button]
            
            choice = self._wait_for_choice(self.player, choices)

            if choice == return_button:
                self._transition_to_scene("MainMenuScene")
                return
            elif choice == quit_button:
                self._quit_whole_game()
                return
