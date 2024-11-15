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
                    print(f"exiting scene via transition")
                except RandomModeGracefulExit:
                    print(f"exiting via random mode counter")
                else:
                    assert mock_transition.called or mock_quit.called
                    if mock_quit.called:
                        print("exiting via quit")
                    if mock_transition.called:
                        print("exiting via transition")
                finally:
                    mock_transition.reset_mock()
                    mock_quit.reset_mock()
