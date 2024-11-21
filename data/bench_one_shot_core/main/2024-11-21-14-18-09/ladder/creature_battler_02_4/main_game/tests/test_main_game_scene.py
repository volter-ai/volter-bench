import pytest
from unittest.mock import Mock, patch
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit
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
            main_game_scene = MainGameScene(app, player)

            # Mock the quit_whole_game method to prevent the exception
            with patch.object(MainGameScene, '_quit_whole_game') as mock_quit:
                try:
                    main_game_scene.run()
                except RandomModeGracefulExit:
                    print(f"random_mode_counter reached 0, ending run {i} gracefully")
                else:
                    # Assert that we exited the scene by quitting
                    assert mock_quit.called, "scene did not end by quitting as expected"
                    print("_quit_whole_game called")
                finally:
                    # Reset the mock for next iteration
                    mock_quit.reset_mock()
