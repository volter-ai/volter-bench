from mini_game_engine.engine.lib import AbstractGameScene, Button

class MainMenuScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.example_variable = 0

    def __str__(self):
        return f"""===Main Menu===
Welcome to creature_battler_04_4

example variable: {self.example_variable}
> Play
> Quit
"""

    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            default_behavior_button = Button("Play")
            quit_button = Button("Quit")
            choices = [
                default_behavior_button,
                quit_button
            ]
            choice = self._wait_for_choice(self.player, choices)

            if default_behavior_button == choice:
                self._transition_to_scene("MainGameScene")  # Transition to MainGameScene
            elif quit_button == choice:
                self._quit_whole_game()
