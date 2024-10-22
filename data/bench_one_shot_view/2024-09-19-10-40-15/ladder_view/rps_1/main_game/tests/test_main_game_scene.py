from unittest.mock import patch

import pytest
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.lib import HumanListener


class TestMainGameSceneRandomRun:
    @pytest.fixture
    def app(self):
        return App()

    def test_main_game_scene_random_run(self, app):
        HumanListener.random_mode = True

        # Patch the transition_to_scene method
        with patch.object(App, 'transition_to_scene') as mock_transition:
            for i in range(10):
                player = app.create_player(f"player_{i}")
                main_game_scene = MainGameScene(app, player)

                main_game_scene.run()

                # Assert that transition_to_scene was called
                assert mock_transition.called

                # Reset the mock calls for the next iteration
                mock_transition.reset_mock()
