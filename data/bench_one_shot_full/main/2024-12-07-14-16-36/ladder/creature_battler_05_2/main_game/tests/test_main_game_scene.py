import pytest
from unittest.mock import Mock, patch

from mini_game_engine.engine.lib import HumanListener, AbstractApp, RandomModeGracefulExit
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
            main_game_scene = MainGameScene(app, player)

            try:
                main_game_scene.run()
            except (RandomModeGracefulExit, AbstractApp._QuitWholeGame):
                # Both are valid ways for the random test to end
                print(f"Game ended gracefully in run {i}")
            except Exception as e:
                # Now this will only catch truly unexpected errors
                pytest.fail(f"Unexpected error in run {i}: {str(e)}")
