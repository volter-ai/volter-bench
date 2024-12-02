import pytest
from unittest.mock import patch
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit, AbstractApp
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
            HumanListener.random_mode_counter = 30  # More moves needed for battle scene

            player = app.create_player(f"player_{i}")
            scene = MainGameScene(app, player)

            with patch.object(MainGameScene, '_quit_whole_game') as mock_quit:
                try:
                    scene.run()
                except RandomModeGracefulExit:
                    print(f"random mode counter reached 0 in run {i}")
                except AbstractApp._QuitWholeGame:
                    print(f"game quit gracefully in run {i}")
                else:
                    # Assert that we exited the scene by quitting
                    assert mock_quit.called, "scene did not exit by quitting"
                    print("_quit_whole_game called")
                finally:
                    mock_quit.reset_mock()
