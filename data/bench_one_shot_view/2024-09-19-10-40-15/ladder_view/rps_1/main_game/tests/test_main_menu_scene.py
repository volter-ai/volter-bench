from unittest.mock import patch

import pytest
from main_game.main import App
from main_game.scenes.main_menu_scene import MainMenuScene
from mini_game_engine.engine.lib import HumanListener


class TestMainMenuSceneRandomRun:
    @pytest.fixture
    def app(self):
        return App()

    def test_main_menu_scene_random_run(self, app):
        HumanListener.random_mode = True

        # Patch the transition_to_scene and quit_whole_game methods
        with patch.object(App, 'transition_to_scene') as mock_transition, \
                patch.object(App, 'quit_whole_game') as mock_quit:
            for i in range(10):
                player = app.create_player(f"player_{i}")
                main_menu_scene = MainMenuScene(app, player)

                main_menu_scene.run()

                # Assert that either transition_to_scene or quit_whole_game was called
                assert mock_transition.called or mock_quit.called

                # Reset the mock calls for the next iteration
                mock_transition.reset_mock()
                mock_quit.reset_mock()
