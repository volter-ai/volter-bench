import pytest
from unittest.mock import patch
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit, GracefulExit
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

            # Patch quit_whole_game to track if it was called
            with patch.object(MainGameScene, '_quit_whole_game') as mock_quit:
                try:
                    main_game_scene.run()
                except RandomModeGracefulExit:
                    print(f"Random mode completed successfully for run {i}")
                except GracefulExit:
                    print(f"Game ended gracefully for run {i}")
                    assert mock_quit.called, "Game ended but _quit_whole_game was not called"
                else:
                    assert mock_quit.called, "Scene ended without calling _quit_whole_game"
