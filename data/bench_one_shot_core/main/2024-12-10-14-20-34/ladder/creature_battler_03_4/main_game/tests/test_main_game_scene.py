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
            HumanListener.random_mode_counter = 30  # Need more moves for battle scene

            player = app.create_player(f"player_{i}")
            game_scene = MainGameScene(app, player)

            class TransitionFromScene(Exception):
                pass

            def exit_scene(*args, **kwargs):
                raise TransitionFromScene()

            with patch.object(MainGameScene, '_transition_to_scene', side_effect=exit_scene) as mock_transition, \
                    patch.object(MainGameScene, '_quit_whole_game') as mock_quit:

                try:
                    game_scene.run()
                except TransitionFromScene:
                    print(f"Scene transition occurred in run {i}")
                except RandomModeGracefulExit:
                    print(f"Random mode completed successfully for run {i}")
                else:
                    assert mock_transition.called or mock_quit.called, "Scene was not exited in an expected manner"
                    if mock_quit.called:
                        print("Game ended via _quit_whole_game")
                    if mock_transition.called:
                        print("Game ended via _transition_to_scene")
                finally:
                    mock_transition.reset_mock()
                    mock_quit.reset_mock()
