import pytest
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene

def test_main_game_scene_random_run():
    for i in range(10):
        print(f"Starting random run iteration {i}")
        HumanListener.random_mode = True
        HumanListener.random_mode_counter = 30  # More moves needed for battle
        
        app = App()
        player = app.create_player(f"player_{i}")
        scene = MainGameScene(app, player)
        
        try:
            scene.run()
        except RandomModeGracefulExit:
            print(f"Random mode completed successfully for iteration {i}")
