import pytest
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
            HumanListener.random_mode_counter = 30  # More moves needed for complex battle scene

            player = app.create_player(f"player_{i}")
            scene = MainGameScene(app, player)

            try:
                scene.run()
            except AbstractApp._QuitWholeGame:
                print("Game ended gracefully via _QuitWholeGame")
            except RandomModeGracefulExit:
                print("Random mode counter reached 0")
            else:
                pytest.fail("Scene did not end with expected exception")
