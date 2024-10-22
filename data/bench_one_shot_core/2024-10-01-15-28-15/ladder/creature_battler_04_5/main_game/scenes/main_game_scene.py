from main_game.models import Player
from main_game.tests.test_main_game_scene import BattleCompletedEvent
from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainGameScene(AbstractGameScene):
    def __init__(self, app: "AbstractApp", player: Player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.battles_played = 0
        self.max_battles = 3

    def __str__(self):
        return (
            f"Player: {self.player.display_name}\n"
            f"Creature: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})\n"
            f"Opponent: {self.opponent.display_name}\n"
            f"Creature: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})\n"
            f"Battles played: {self.battles_played}/{self.max_battles}\n"
        )

    def run(self):
        while self.battles_played < self.max_battles:
            self._reset_creatures()
            self._run_battle()
            self.battles_played += 1
            AbstractApp.broadcast_event(BattleCompletedEvent())
            
            if self.battles_played < self.max_battles:
                self._show_text(self.player, f"Battle {self.battles_played} completed. Starting next battle...")
                choice = self._wait_for_choice(self.player, [Button("Continue")])
            else:
                self._show_text(self.player, "All battles completed!")
                self._transition_to_scene("MainMenuScene")

    # ... (rest of the methods remain the same)
