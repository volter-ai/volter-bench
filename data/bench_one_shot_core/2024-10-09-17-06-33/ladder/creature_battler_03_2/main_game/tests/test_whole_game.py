import os
import sys

from main_game.main import App
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit


def test_full_game_flow_random_with_bots():
    for i in range(10):
        print(f"starting random run iteration {i}")
        HumanListener.random_mode = True
        HumanListener.random_mode_counter = 100  # 100 moves suffice for running through some common scenarios in the game
        App.matchmaking_wait_time = 0
        original_wait_time = App.matchmaking_wait_time

        app = App()

        # Create a human player
        human_player = app.create_player("HumanPlayer")
        human_player.set_listener(HumanListener())

        try:
            app.run(human_player)
        except RandomModeGracefulExit as e:
            # exited gracefully
            pass
        finally:
            App.matchmaking_wait_time = original_wait_time

