import pytest
from unittest.mock import patch

from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit
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
            HumanListener.random_mode_counter = 30  # Battle scenes need more moves

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            class GracefulGameEnd(Exception):
                pass

            def exit_game(*args, **kwargs):
                raise GracefulGameEnd()

            # Patch quit_whole_game to raise our test exception instead
            with patch.object(MainGameScene, '_quit_whole_game', side_effect=exit_game):
                try:
                    main_game_scene.run()
                except GracefulGameEnd:
                    print(f"Game ended gracefully in run {i}")
                except RandomModeGracefulExit:
                    print(f"`random_mode_counter` reached 0 and the game did not crash. Ending run {i} gracefully")
