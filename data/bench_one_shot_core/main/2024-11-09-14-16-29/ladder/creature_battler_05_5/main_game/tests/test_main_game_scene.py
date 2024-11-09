import pytest
from unittest.mock import Mock, patch

from mini_game_engine.engine.lib import HumanListener, GracefulExit, RandomModeGracefulExit, AbstractApp
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
            HumanListener.random_mode_counter = 30  # Need more moves for complex battle scene

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            try:
                main_game_scene.run()
            except RandomModeGracefulExit:
                print(f"`random_mode_counter` reached 0 and the game did not crash. Ending run {i} gracefully")
            except AbstractApp._QuitWholeGame:
                print(f"Game completed successfully via main menu quit. Ending run {i} gracefully")
            except Exception as e:
                pytest.fail(f"Unexpected exception during run {i}: {str(e)}")
