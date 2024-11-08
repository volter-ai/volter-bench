import pytest
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit, AbstractApp
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
            
            try:
                app.transition_to_scene("MainGameScene", player=player)
            except (RandomModeGracefulExit, AbstractApp._QuitWholeGame) as e:
                print(f"Run {i} completed successfully with expected exit: {str(e)}")
            except Exception as e:
                pytest.fail(f"Unexpected error in run {i}: {str(e)}")
