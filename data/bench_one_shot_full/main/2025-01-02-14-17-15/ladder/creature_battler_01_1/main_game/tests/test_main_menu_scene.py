import pytest
from unittest.mock import patch
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit
from main_game.main import App
from main_game.scenes.main_menu_scene import MainMenuScene

class TestMainMenuScene:
    @pytest.fixture
    def app(self):
        return App()

    def test_main_menu_scene_random_run(self, app):
        for _ in range(10):
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 10
            player = app.create_player("test_player")
            scene = MainMenuScene(app, player)

            with patch.object(scene, '_transition_to_scene') as mock_transition, \
                 patch.object(scene, '_quit_whole_game') as mock_quit:
                try:
                    scene.run()
                except RandomModeGracefulExit:
                    pass
                assert mock_transition.called or mock_quit.called
