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
            HumanListener.random_mode_counter = 30  # More moves needed for battle scene

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            try:
                main_game_scene.run()
            except RandomModeGracefulExit:
                print(f"Random mode counter reached 0. Ending run {i}")
            except AbstractApp._QuitWholeGame:
                print(f"Game quit after battle completion. Ending run {i}")
            finally:
                # Always reset creature HP for next iteration
                for creature in player.creatures:
                    creature.hp = creature.max_hp
                for creature in main_game_scene.opponent.creatures:
                    creature.hp = creature.max_hp
