import pytest
from unittest.mock import patch
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit
from main_game.scenes.main_game_scene import MainGameScene
from main_game.main import App

class TestMainGameSceneRandomRun:
    @pytest.fixture
    def app(self):
        return App()

    def test_main_game_scene_random_run(self, app):
        for i in range(10):
            print(f"Starting random run iteration {i}")
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 30  # More moves needed for battle scene

            player = app.create_player(f"player_{i}")
            scene = MainGameScene(app, player)

            class GameEnd(Exception):
                pass

            def exit_game(*args, **kwargs):
                raise GameEnd()

            with patch.object(MainGameScene, '_quit_whole_game', side_effect=exit_game) as mock_quit:
                try:
                    scene.run()
                except GameEnd:
                    print(f"Game ended normally in run {i}")
                except RandomModeGracefulExit:
                    print(f"Random mode completed run {i}")
                else:
                    assert mock_quit.called, "Game did not end properly"
                finally:
                    mock_quit.reset_mock()
