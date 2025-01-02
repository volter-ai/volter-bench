import pytest
from unittest.mock import patch
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit
from main_game.scenes.main_menu_scene import MainMenuScene
from main_game.main import App

class TestMainMenuSceneRandomRun:
    @pytest.fixture
    def app(self):
        return App()

    def test_main_menu_scene_random_run(self, app):
        for i in range(10):
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 10

            player = app.create_player(f"player_{i}")
            main_menu_scene = MainMenuScene(app, player)

            with patch.object(MainMenuScene, '_transition_to_scene', side_effect=Exception("Transition")) as mock_transition, \
                 patch.object(MainMenuScene, '_quit_whole_game', side_effect=Exception("Quit")) as mock_quit:

                try:
                    main_menu_scene.run()
                except (Exception, RandomModeGracefulExit) as e:
                    assert str(e) in ["Transition", "Quit", "RandomModeGracefulExit"]
