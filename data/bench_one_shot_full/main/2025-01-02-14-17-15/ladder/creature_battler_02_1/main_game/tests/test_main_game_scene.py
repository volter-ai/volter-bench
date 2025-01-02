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
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 30

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            with patch.object(MainGameScene, '_show_text') as mock_show_text:
                try:
                    main_game_scene.run()
                except RandomModeGracefulExit:
                    pass
                except AbstractApp._QuitWholeGame:
                    # Handle the expected quit exception gracefully
                    print("Game terminated gracefully as expected.")
                else:
                    assert mock_show_text.called
