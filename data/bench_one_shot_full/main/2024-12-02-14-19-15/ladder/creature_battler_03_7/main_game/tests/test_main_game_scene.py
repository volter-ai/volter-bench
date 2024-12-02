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
            print(f"Starting random run iteration {i}")
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 30  # More moves needed for battle scene

            player = app.create_player(f"player_{i}")
            scene = MainGameScene(app, player)

            class QuitGame(Exception):
                pass

            def exit_game(*args, **kwargs):
                raise QuitGame()

            with patch.object(MainGameScene, '_quit_whole_game', side_effect=exit_game) as mock_quit:
                try:
                    scene.run()
                except RandomModeGracefulExit:
                    print(f"Random mode counter reached 0, ending run {i}")
                except QuitGame:
                    print(f"Game ended naturally through battle completion, ending run {i}")
                    assert mock_quit.called, "Game ended but _quit_whole_game wasn't called"
                else:
                    assert False, "Scene ended without expected exit condition"

                mock_quit.reset_mock()
