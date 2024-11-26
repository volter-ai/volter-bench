import pytest
from unittest.mock import patch
from mini_game_engine.engine.lib import (
    HumanListener, 
    RandomModeGracefulExit,
    AbstractApp
)
from main_game.scenes.main_game_scene import MainGameScene
from main_game.main import App

class TestMainGameSceneRandomRun:
    @pytest.fixture
    def app(self):
        return App()

    def test_main_game_scene_random_run(self, app):
        for i in range(10):
            print(f"Starting random run iteration {i}")
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 30  # More moves needed for complex battle scene

            player = app.create_player(f"player_{i}")
            scene = MainGameScene(app, player)

            try:
                scene.run()
            except RandomModeGracefulExit:
                print(f"Random mode counter reached 0 in run {i}")
            except AbstractApp._QuitWholeGame:
                print(f"Battle completed normally in run {i}")
            else:
                pytest.fail("Scene ended without expected transition or game end")
