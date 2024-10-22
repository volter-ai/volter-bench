from mini_game_engine.engine.lib import AbstractGameScene, Button


class BattleResultScene(AbstractGameScene):
    def __init__(self, app, player, previous_scene):
        super().__init__(app, player)
        self.winner = previous_scene.battle_winner if hasattr(previous_scene, 'battle_winner') else None

    def __str__(self):
        result = "You win!" if self.winner == self.player else "You lose!"
        return f"""===Battle Result===
{result}

> Return to Main Menu
> Quit Game
"""

    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            main_menu_button = Button("Return to Main Menu")
            quit_button = Button("Quit Game")
            choices = [main_menu_button, quit_button]
            choice = self._wait_for_choice(self.player, choices)

            if choice == main_menu_button:
                self._transition_to_scene("MainMenuScene")
                return
            elif choice == quit_button:
                self._quit_whole_game()
                return
