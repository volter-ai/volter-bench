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
            HumanListener.random_mode_counter = 30  # Need more moves for battle scene

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            # Patch quit_whole_game to track if it was called
            with patch.object(AbstractApp, 'quit_whole_game') as mock_quit:
                try:
                    main_game_scene.run()
                except RandomModeGracefulExit:
                    print(f"Random mode counter reached 0. Ending run {i}")
                except AbstractApp._QuitWholeGame:
                    print(f"Game ended gracefully in run {i}")
                
                # Assert that either the game ended naturally or random mode expired
                assert mock_quit.called or HumanListener.random_mode_counter <= 0, \
                    "Scene did not end properly"
