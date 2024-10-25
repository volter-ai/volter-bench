from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainMenuScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.example_variable = 0

    def __str__(self):
        # all the information relevant to the usage of the scene should be displayed here
        return f"""===Main Menu===
Welcome to creature_battler_03_6

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
                self.example_variable = 1 - self.example_variable  # toggle example variable
                # self._transition_to_scene("SceneName")  # do this to transition to a scene
            elif quit_button == choice:
                self._quit_whole_game()
