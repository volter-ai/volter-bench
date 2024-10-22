from mini_game_engine.engine.lib import AbstractGameScene, AbstractApp


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""
Creature Battle!

{self.player.display_name}'s {self.player.active_creature.display_name}:
HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp}

{self.opponent.display_name}'s {self.opponent.active_creature.display_name}:
HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp}

1. Attack
2. Swap
"""

    def run(self):
        try:
            while True:
                self._show_text(self.player, str(self))
                self._show_text(self.opponent, str(self))

                player_action = self.player_choice_phase(self.player)
                opponent_action = self.player_choice_phase(self.opponent)

                self.resolution_phase(player_action, opponent_action)

                if self.check_battle_end():
                    break

            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
        except AbstractApp._QuitWholeGame:
            self._show_text(self.player, "Battle ended. Returning to main menu.")
            raise

    # ... (rest of the MainGameScene code remains unchanged)
