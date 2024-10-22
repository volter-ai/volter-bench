import pytest
from unittest.mock import Mock, patch

from mini_game_engine.engine.lib import HumanListener, GracefulExit, RandomModeGracefulExit
from main_game.scenes.main_menu_scene import MainMenuScene
from main_game.main import App


class TestMainMenuSceneRandomRun:
    @pytest.fixture
    def app(self):
        return App()

    def test_main_menu_scene_random_run(self, app):
        for i in range(10):
            print(f"starting random run iteration {i}")
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 10  # 10 moves should suffice for testing a simple scene like main menu. More complex scenes might need 30 or more moves, it depends on the scene

            player = app.create_player(f"player_{i}")
            main_game_scene = MainMenuScene(app, player)

            class TransitionFromScene(Exception):
                pass

            def exit_scene(*args, **kwargs):
                raise TransitionFromScene()

            # patch the two ways of exiting the scene so we can catch them. When we exit the scene, the run is over
            with patch.object(MainMenuScene, '_transition_to_scene', side_effect=exit_scene) as mock_transition, \
                    patch.object(MainMenuScene, '_quit_whole_game') as mock_quit:

                try:
                    main_game_scene.run()
                except TransitionFromScene:
                    print(f"exiting target scene `MainMenuScene` so ending run {i}")
                except RandomModeGracefulExit:
                    print(f"`random_mode_counter` reached 0 and the game did not crash. Ending run {i} gracefully")
                else:
                    # assert that we exited the scene in one of the expected ways
                    assert mock_transition.called or mock_quit.called, "scene was not exited in an expected manner"

                    # important to print how we exited the scene, for debug purposes
                    if mock_quit.called:
                        print("_quit_whole_game called")
                    if mock_transition.called:
                        print("_transition_to_scene called")
                finally:
                    # Reset the mock calls for the next iteration
                    mock_transition.reset_mock()
                    mock_quit.reset_mock()
