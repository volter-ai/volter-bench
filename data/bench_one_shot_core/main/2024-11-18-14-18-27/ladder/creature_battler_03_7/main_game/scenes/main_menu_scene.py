from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.scenes.main_game_scene import MainGameScene

class MainMenuScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self._app.register_scene("MainGameScene", MainGameScene)

    def __str__(self):
        return """=== Creature Battler ===
Welcome! Choose an option:

1. Play Game
2. Quit
"""

    def run(self):
        self._show_text(self.player, "Welcome to Creature Battler!")
        
        while True:
            choice = self._wait_for_choice(self.player, [
                Button("Play Game"),
                Button("Quit")
            ])

            if choice.display_name == "Play Game":
                self._transition_to_scene("MainGameScene")
            else:
                self._quit_whole_game()
