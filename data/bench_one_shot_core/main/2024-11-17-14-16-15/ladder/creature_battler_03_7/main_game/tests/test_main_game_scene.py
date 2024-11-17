import pytest
from unittest.mock import patch
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit, GracefulExit
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

            with patch.object(MainGameScene, '_transition_to_scene', side_effect=exit_scene) as mock_transition, \
                    patch.object(MainGameScene, '_quit_whole_game') as mock_quit:

                try:
                    main_game_scene.run()
                except (TransitionFromScene, RandomModeGracefulExit, GracefulExit) as e:
                    print(f"Scene ended with: {type(e).__name__}")
                finally:
                    # Assert that we exited the scene in one of the expected ways
                    assert mock_transition.called or mock_quit.called, "Scene did not exit properly"
                    
                    # Reset mocks for next iteration
                    mock_transition.reset_mock()
                    mock_quit.reset_mock()
