import pytest
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit
from main_game.main import App
from unittest.mock import patch

def test_main_menu_scene_random_run():
    app = App()
    
    for i in range(10):
        print(f"Starting random run iteration {i}")
        HumanListener.random_mode = True
        HumanListener.random_mode_counter = 10
        
        player = app.create_player(f"player_{i}")
        
        try:
            app.run(player)
        except RandomModeGracefulExit:
            print(f"Random mode completed successfully for run {i}")
