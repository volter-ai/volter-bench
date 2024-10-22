import random

from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainMenuScene(AbstractGameScene):
    def __str__(self):
        return "Welcome to Creature Battle!\n1. Play\n2. Quit"

    def run(self):
        self._show_text(self.player, "Welcome to Creature Battle!")
        choices = [
            Button("Play"),
            Button("Quit")
        ]
        
        print(f"Available choices: {[choice.display_name for choice in choices]}")  # Debug print
        
        choice = self._wait_for_choice(self.player, choices)

        print(f"Player chose: {choice.display_name}")  # Debug print

        if choice.display_name == "Play":
            print("Transitioning to MainGameScene")  # Debug print
            self._transition_to_scene("MainGameScene")
        elif choice.display_name == "Quit":
            print("Quitting the game")  # Debug print
            self._quit_whole_game()
        else:
            print(f"Unexpected choice: {choice.display_name}")  # Debug print

    def _wait_for_choice(self, player, choices):
        if player._listener.random_mode:
            # In random mode, we want to test both "Play" and "Quit" scenarios
            # We'll use a 2:1 ratio in favor of "Play" to ensure we test the transition more often
            return random.choices(choices, weights=[2, 1])[0]
        else:
            return super()._wait_for_choice(player, choices)
