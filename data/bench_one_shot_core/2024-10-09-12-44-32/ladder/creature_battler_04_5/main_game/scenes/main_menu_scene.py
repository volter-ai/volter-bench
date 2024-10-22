from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainMenuScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)

    def __str__(self):
        return """===Main Menu===
Welcome to Creature Battler

> Play
> Quit
"""

    def run(self):
        self._show_text(self.player, "Welcome to Creature Battler")
        while True:
            play_button = Button("Play")
            quit_button = Button("Quit")
            choices = [play_button, quit_button]
            choice = self._wait_for_choice(self.player, choices)

            if choice == play_button:
                self._transition_to_scene("MainGameScene")
            elif choice == quit_button:
                self._quit_whole_game()
