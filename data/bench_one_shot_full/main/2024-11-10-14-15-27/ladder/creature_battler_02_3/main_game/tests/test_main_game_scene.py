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
            HumanListener.random_mode_counter = 30

            player = app.create_player(f"player_{i}")
            scene = MainGameScene(app, player)

            with patch.object(MainGameScene, '_quit_whole_game') as mock_quit:
                try:
                    scene.run()
                except RandomModeGracefulExit:
                    print(f"random mode counter reached 0, ending run {i}")
                else:
                    assert mock_quit.called
                    print("_quit_whole_game called")
                finally:
                    mock_quit.reset_mock()
