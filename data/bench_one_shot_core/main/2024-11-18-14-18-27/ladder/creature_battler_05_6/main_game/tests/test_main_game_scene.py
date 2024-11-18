import pytest
from unittest.mock import Mock, patch

from mini_game_engine.engine.lib import (
    HumanListener, 
    GracefulExit, 
    RandomModeGracefulExit,
    AbstractApp
)
from main_game.scenes.main_game_scene import MainGameScene
from main_game.main import App

class TestMainGameSceneRandomRun:
    @pytest.fixture
    def app(self):
        return App()

    def test_main_game_scene_random_run(self, app):
        for i in range(10):
            print(f"starting random run iteration {i}")
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 30  # Need more moves for battle scene

            player = app.create_player(f"player_{i}")
            scene = MainGameScene(app, player)

            try:
                scene.run()
            except (RandomModeGracefulExit, AbstractApp._QuitWholeGame) as e:
                # Both of these exceptions are expected ways for the scene to end
                print(f"Scene ended gracefully for run {i}: {str(e)}")
            except Exception as e:
                # Only fail on unexpected exceptions
                pytest.fail(f"Unexpected error in run {i}: {str(e)}")
