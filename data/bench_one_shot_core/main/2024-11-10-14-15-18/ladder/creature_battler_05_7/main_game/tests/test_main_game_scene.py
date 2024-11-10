import pytest
from unittest.mock import Mock, patch

from mini_game_engine.engine.lib import HumanListener, GracefulExit, RandomModeGracefulExit
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
            main_game_scene = MainGameScene(app, player)

            # Patch the transition method to prevent actual scene transition
            with patch.object(MainGameScene, '_transition_to_scene') as mock_transition:
                try:
                    main_game_scene.run()
                except RandomModeGracefulExit:
                    print(f"`random_mode_counter` reached 0 and the game did not crash. Ending run {i} gracefully")
                
                # Verify that the scene attempted to transition back to menu
                assert mock_transition.called
                assert mock_transition.call_args[0][0] == "MainMenuScene", "Scene should transition back to main menu"
