import pytest
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit, AbstractApp
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene


class TestMainGameSceneRandomRun:
    @pytest.fixture
    def app(self):
        return App()

    def test_main_game_scene_random_run(self, app):
        for i in range(10):
            print(f"starting random run iteration {i}")
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 100  # Increased to ensure all battles and menu interactions complete

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            try:
                main_game_scene.run()
            except AbstractApp._QuitWholeGame:
                print("Game ended gracefully")
            except RandomModeGracefulExit:
                print(f"`random_mode_counter` reached 0 and the game did not crash. Ending run {i} gracefully")
            
            # Assert that all battles were completed
            assert main_game_scene.battle_count == main_game_scene.max_battles, f"Not all battles were completed. Only {main_game_scene.battle_count} out of {main_game_scene.max_battles} were played."
            
            # Assert that the game returned to the main menu
            assert isinstance(app._current_scene, type(app.scene_registry["MainMenuScene"](app, player))), "Game did not return to the main menu after battles"
            
            # Assert that the game count in the main menu was incremented
            assert app._current_scene.game_count > 0, "Game count in main menu was not incremented"

            print(f"Run {i} completed successfully")
