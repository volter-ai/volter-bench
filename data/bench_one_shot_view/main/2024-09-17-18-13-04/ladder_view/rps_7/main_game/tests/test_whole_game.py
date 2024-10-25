import os
import sys

from mini_game_engine.engine.lib import HumanListener
from main_game.main import App


def test_full_game_flow_random_with_bots():
    HumanListener.random_mode = True
    App.matchmaking_wait_time = 0
    original_wait_time = App.matchmaking_wait_time

    for i in range(10):
        app = App()

        # Create a human player
        human_player = app.create_player("HumanPlayer")
        human_player.set_listener(HumanListener())

        app.run(human_player)

    App.matchmaking_wait_time = original_wait_time
