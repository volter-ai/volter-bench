from mini_game_engine.engine.lib import AbstractGameScene, Button

class MainMenuScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)

    def __str__(self):
        return """=== Creature Battler ===
Welcome! Choose an option:
> Play - Start a battle
> Quit - Exit game
"""

    def run(self):
        self._show_text(self.player, "Welcome to Creature Battler!")
        
        while True:
            play_button = Button("Play")
            quit_button = Button("Quit")
            choice = self._wait_for_choice(self.player, [play_button, quit_button])

            if choice == play_button:
                self._transition_to_scene("MainGameScene")
            elif choice == quit_button:
                self._quit_whole_game()
