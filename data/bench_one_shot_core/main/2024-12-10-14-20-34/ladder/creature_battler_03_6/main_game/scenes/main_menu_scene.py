from mini_game_engine.engine.lib import AbstractGameScene, Button

class MainMenuScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)

    def __str__(self):
        return """=== Creature Battler ===
Welcome! Choose an option:
> Play
> Quit
"""

    def run(self):
        self.game_loop()

    def game_loop(self):
        while True:
            play_button = Button("Play")
            quit_button = Button("Quit")
            choices = [play_button, quit_button]
            
            choice = self._wait_for_choice(self.player, choices)

            if play_button == choice:
                self._transition_to_scene("MainGameScene")
            elif quit_button == choice:
                self._quit_whole_game()
