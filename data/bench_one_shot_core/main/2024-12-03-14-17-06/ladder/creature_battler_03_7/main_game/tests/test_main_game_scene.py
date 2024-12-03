import pytest
from unittest.mock import Mock, patch

from mini_game_engine.engine.lib import HumanListener, GracefulExit, RandomModeGracefulExit
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

            class QuitGame(Exception):
                pass

            def exit_game(*args, **kwargs):
                raise QuitGame()

            with patch.object(MainGameScene, '_quit_whole_game', side_effect=exit_game) as mock_quit:
                try:
                    main_game_scene.run()
                except QuitGame:
                    print(f"Game quit gracefully in run {i}")
                except RandomModeGracefulExit:
                    print(f"`random_mode_counter` reached 0 and the game did not crash. Ending run {i} gracefully")
                else:
                    assert mock_quit.called, "Game did not end properly"
                finally:
                    mock_quit.reset_mock()
