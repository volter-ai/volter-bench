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
            HumanListener.random_mode_counter = 30

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            try:
                main_game_scene.run()
            except (RandomModeGracefulExit, AbstractApp._QuitWholeGame) as e:
                print(f"Run {i} completed successfully with: {str(e)}")
                continue
            except Exception as e:
                raise e  # Re-raise unexpected exceptions
