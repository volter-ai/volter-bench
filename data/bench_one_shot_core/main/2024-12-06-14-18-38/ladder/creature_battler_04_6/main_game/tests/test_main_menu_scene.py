import pytest
from unittest.mock import patch

from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit
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
            HumanListener.random_mode_counter = 10

            player = app.create_player(f"player_{i}")
            scene = MainMenuScene(app, player)

            class TransitionFromScene(Exception):
                pass

            def exit_scene(*args, **kwargs):
                raise TransitionFromScene()

            with patch.object(MainMenuScene, '_transition_to_scene', side_effect=exit_scene) as mock_transition, \
                 patch.object(MainMenuScene, '_quit_whole_game') as mock_quit:

                try:
                    scene.run()
                except TransitionFromScene:
                    print(f"exiting target scene `MainMenuScene` so ending run {i}")
                except RandomModeGracefulExit:
                    print(f"`random_mode_counter` reached 0 and the game did not crash. Ending run {i} gracefully")
                else:
                    assert mock_transition.called or mock_quit.called

                    if mock_quit.called:
                        print("_quit_whole_game called")
                    if mock_transition.called:
                        print("_transition_to_scene called")
                finally:
                    mock_transition.reset_mock()
                    mock_quit.reset_mock()
