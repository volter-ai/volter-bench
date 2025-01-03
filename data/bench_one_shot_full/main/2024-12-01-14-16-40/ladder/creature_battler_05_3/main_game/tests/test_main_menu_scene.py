import pytest
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit
from main_game.main import App
from unittest.mock import patch

def test_main_menu_scene_random():
    for i in range(10):
        HumanListener.random_mode = True
        HumanListener.random_mode_counter = 10
        
        app = App()
        player = app.create_player(f"test_player_{i}")
        
        try:
            app.run(player)
        except RandomModeGracefulExit:
            print(f"Random run {i} completed successfully")
