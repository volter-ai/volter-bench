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
            HumanListener.random_mode_counter = 30  # More moves needed for battle scene

            player = app.create_player(f"player_{i}")
            scene = MainGameScene(app, player)

            class QuitFromScene(Exception):
                pass

            def exit_game(*args, **kwargs):
                raise QuitFromScene()

            with patch.object(MainGameScene, '_quit_whole_game', side_effect=exit_game) as mock_quit:
                try:
                    scene.run()
                except QuitFromScene:
                    print(f"game ended via quit in run {i}")
                except RandomModeGracefulExit:
                    print(f"random mode counter reached 0 in run {i}")
                else:
                    assert False, "Scene did not end through an expected path"

                assert mock_quit.called, "Game should have ended with _quit_whole_game"
                mock_quit.reset_mock()
