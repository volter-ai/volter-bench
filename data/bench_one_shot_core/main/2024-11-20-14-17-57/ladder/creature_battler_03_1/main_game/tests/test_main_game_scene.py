import pytest
from unittest.mock import patch

from mini_game_engine.engine.lib import RandomModeGracefulExit, HumanListener, AbstractApp
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
            game_scene = MainGameScene(app, player)

            class TransitionFromScene(Exception):
                pass

            def exit_scene(*args, **kwargs):
                raise TransitionFromScene()

            # Patch both transition and quit methods to catch all exit conditions
            with patch.object(MainGameScene, '_transition_to_scene', side_effect=exit_scene) as mock_transition, \
                 patch.object(MainGameScene, '_quit_whole_game') as mock_quit:

                try:
                    game_scene.run()
                except TransitionFromScene:
                    print(f"Scene transitioned to another scene, ending run {i}")
                except RandomModeGracefulExit:
                    print(f"Random mode counter reached 0, ending run {i}")
                except AbstractApp._QuitWholeGame:
                    print(f"Game quit gracefully, ending run {i}")
                else:
                    # Assert that we exited the scene in one of the expected ways
                    assert mock_transition.called or mock_quit.called, "Scene was not exited in an expected manner"

                    if mock_quit.called:
                        print("_quit_whole_game called")
                    if mock_transition.called:
                        print("_transition_to_scene called")
                finally:
                    # Reset the mock calls for the next iteration
                    mock_transition.reset_mock()
                    mock_quit.reset_mock()
