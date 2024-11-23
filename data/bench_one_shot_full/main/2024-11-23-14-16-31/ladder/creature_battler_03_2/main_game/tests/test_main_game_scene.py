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
            print(f"starting random run iteration {i}")
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 30

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            class TransitionFromScene(Exception):
                pass

            def exit_scene(*args, **kwargs):
                raise TransitionFromScene()

            # Mock both ways to exit the scene
            with patch.object(MainGameScene, '_quit_whole_game', side_effect=exit_scene) as mock_quit:
                try:
                    main_game_scene.run()
                except TransitionFromScene:
                    print(f"exiting scene via quit, ending run {i}")
                except RandomModeGracefulExit:
                    print(f"random_mode_counter reached 0, ending run {i}")
                else:
                    assert mock_quit.called, "scene did not exit as expected"
                finally:
                    mock_quit.reset_mock()
