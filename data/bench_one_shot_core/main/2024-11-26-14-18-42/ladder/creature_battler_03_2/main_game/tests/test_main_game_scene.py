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
            main_game_scene = MainGameScene(app, player)

            # Mock both possible ways to exit the scene
            with patch.object(MainGameScene, '_quit_whole_game') as mock_quit:
                try:
                    main_game_scene.run()
                except RandomModeGracefulExit:
                    print(f"`random_mode_counter` reached 0 and the game did not crash. Ending run {i} gracefully")
                except AbstractApp._QuitWholeGame:
                    print("Game quit gracefully")
                else:
                    # Assert that we exited the scene by quitting (since this scene only ends via quit)
                    assert mock_quit.called, "scene was not exited via quit"
                    print("_quit_whole_game called")
                finally:
                    # Reset the mock calls for the next iteration
                    mock_quit.reset_mock()
