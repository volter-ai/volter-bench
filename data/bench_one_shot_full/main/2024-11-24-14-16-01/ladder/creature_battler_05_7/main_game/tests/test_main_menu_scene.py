import pytest
from unittest.mock import Mock, patch
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit, AbstractApp
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

            try:
                scene.run()
            except (RandomModeGracefulExit, AbstractApp._QuitWholeGame) as e:
                print(f"Run {i} completed as expected with: {type(e).__name__}")
