import pytest
from unittest.mock import patch

from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit, AbstractApp
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
            scene = MainGameScene(app, player)

            # Patch transition_to_scene to prevent actual scene transitions during test
            with patch.object(MainGameScene, '_transition_to_scene') as mock_transition:
                try:
                    scene.run()
                except RandomModeGracefulExit:
                    print(f"Random mode counter reached 0, ending run {i}")
                except AbstractApp._QuitWholeGame:
                    print(f"Game quit gracefully, ending run {i}")
                
                # Verify that the scene attempted to transition when battle ended
                assert mock_transition.called, "Scene should attempt to transition after battle"
                assert mock_transition.call_args[0][0] == "MainMenuScene", "Should transition to MainMenuScene"
