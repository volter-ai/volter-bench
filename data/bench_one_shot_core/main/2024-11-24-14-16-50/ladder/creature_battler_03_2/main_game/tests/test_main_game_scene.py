import pytest
from unittest.mock import patch
from mini_game_engine.engine.lib import (
    HumanListener, 
    RandomModeGracefulExit,
    AbstractApp
)
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene

class TestMainGameSceneRandomRun:
    @pytest.fixture
    def app(self):
        return App()

    def test_main_game_scene_random_run(self, app):
        for i in range(10):
            print(f"starting random run iteration {i}")
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 30

            player = app.create_player(f"player_{i}")
            game_scene = MainGameScene(app, player)

            try:
                game_scene.run()
            except RandomModeGracefulExit:
                print(f"Random mode completed successfully for run {i}")
            except AbstractApp._QuitWholeGame:
                print(f"Game quit gracefully for run {i}")
            except Exception as e:
                pytest.fail(f"Unexpected error in run {i}: {str(e)}")
