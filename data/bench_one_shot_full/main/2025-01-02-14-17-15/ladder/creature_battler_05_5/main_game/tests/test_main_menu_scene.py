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
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 10

            player = app.create_player(f"player_{i}")
            main_menu_scene = MainMenuScene(app, player)

            class TransitionFromScene(Exception):
                pass

            def exit_scene(*args, **kwargs):
                raise TransitionFromScene()

            with patch.object(MainMenuScene, '_transition_to_scene', side_effect=exit_scene) as mock_transition, \
                    patch.object(MainMenuScene, '_quit_whole_game') as mock_quit:

                try:
                    main_menu_scene.run()
                except TransitionFromScene:
                    pass
                except RandomModeGracefulExit:
                    pass
                else:
                    assert mock_transition.called or mock_quit.called
                finally:
                    mock_transition.reset_mock()
                    mock_quit.reset_mock()
