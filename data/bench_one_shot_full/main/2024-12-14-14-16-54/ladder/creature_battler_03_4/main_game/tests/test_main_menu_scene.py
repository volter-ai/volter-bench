import pytest
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit
from main_game.main import App
from unittest.mock import patch

def test_main_menu_scene_random():
    for i in range(10):
        app = App()
        HumanListener.random_mode = True
        HumanListener.random_mode_counter = 10
        
        try:
            app.run(app.create_player(f"test_player_{i}"))
        except RandomModeGracefulExit:
            print(f"Random run {i} completed successfully")
