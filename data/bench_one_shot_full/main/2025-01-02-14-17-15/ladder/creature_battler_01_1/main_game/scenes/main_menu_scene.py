from mini_game_engine.engine.lib import AbstractGameScene, Button

class MainMenuScene(AbstractGameScene):
    def __str__(self):
        return "===Main Menu===\nWelcome to Creature Battler!\n1: Play\n2: Quit"

    def run(self):
        while True:
            choice = self._wait_for_choice(self.player, [Button("Play"), Button("Quit")])
            if choice.display_name == "Play":
                self._transition_to_scene("MainGameScene")
            elif choice.display_name == "Quit":
                self._quit_whole_game()
