from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.scenes.main_game_scene import MainGameScene

class MainMenuScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        app.register_scene("MainGameScene", MainGameScene)

    def __str__(self):
        return """=== Creature Battler ===
Welcome! Choose an option:
> Play
> Quit
"""

    def run(self):
        while True:
            play_button = Button("Play")
            quit_button = Button("Quit")
            choice = self._wait_for_choice(self.player, [play_button, quit_button])

            if play_button == choice:
                self._transition_to_scene("MainGameScene")
            elif quit_button == choice:
                self._quit_whole_game()
