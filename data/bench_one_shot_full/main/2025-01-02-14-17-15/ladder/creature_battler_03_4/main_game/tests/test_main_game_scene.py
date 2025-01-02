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
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 30

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            with patch.object(MainGameScene, '_transition_to_scene', side_effect=Exception("Transition")) as mock_transition, \
                 patch.object(MainGameScene, '_quit_whole_game', side_effect=Exception("Quit")) as mock_quit:

                try:
                    main_game_scene.run()
                except RandomModeGracefulExit:
                    print(f"RandomModeGracefulExit occurred, ending run {i} gracefully")
                except Exception as e:
                    assert str(e) in ["Transition", "Quit"]
