from mini_game_engine.engine.lib import (AbstractGameScene, Button,
                                         HumanListener)


class MainMenuScene(AbstractGameScene):
    def __str__(self):
        return "Welcome to Creature Battle!\n1. Play\n2. Quit"

    def run(self):
        self._show_text(self.player, "Welcome to Creature Battle!")
        attempts = 0
        max_attempts = 10  # Limit the number of attempts in random mode

        while attempts < max_attempts:
            attempts += 1
            choice = self._wait_for_choice(self.player, [
                Button("Play"),
                Button("Quit")
            ])

            if choice.display_name == "Play":
                self._transition_to_scene("MainGameScene")
                return  # Exit the run method after transitioning
            elif choice.display_name == "Quit":
                if not isinstance(self.player._listener, HumanListener) or not HumanListener.random_mode:
                    self._quit_whole_game()
                else:
                    # In random mode, we'll continue the loop to give a chance for "Play" to be selected
                    continue

        # If we've reached the maximum number of attempts in random mode, transition to MainGameScene
        if isinstance(self.player._listener, HumanListener) and HumanListener.random_mode:
            self._transition_to_scene("MainGameScene")
