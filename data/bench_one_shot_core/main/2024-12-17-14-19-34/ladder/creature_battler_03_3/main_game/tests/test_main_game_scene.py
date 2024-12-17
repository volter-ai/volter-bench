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
            HumanListener.random_mode_counter = 30  # Battle might take more moves

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            quit_called = False

            try:
                main_game_scene.run()
            except RandomModeGracefulExit:
                print(f"`random_mode_counter` reached 0 and the game did not crash. Ending run {i} gracefully")
            except AbstractApp._QuitWholeGame:
                print(f"Game quit gracefully via _quit_whole_game in run {i}")
                quit_called = True
            
            # Assert that the game ended via quit (battle completed)
            assert quit_called, "Game should end via _quit_whole_game when battle completes"
