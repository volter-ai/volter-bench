from unittest.mock import patch

import pytest
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.lib import HumanListener


class TestMainGameSceneRandomRun:
    @pytest.fixture
    def app(self):
        return App()

    def test_main_game_scene_random_run(self, app):
        for i in range(10):
            print(f"starting random run iteration {i}")
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 30  # Increased to 30 for more complex scene

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            with patch.object(MainGameScene, 'check_battle_end', side_effect=[False, False, False, True]), \
                 patch.object(MainGameScene, '_transition_to_scene') as mock_transition, \
                 patch.object(MainGameScene, '_quit_whole_game') as mock_quit:

                main_game_scene.run()

                assert mock_transition.called or mock_quit.called, "Scene did not transition or quit as expected"

                if mock_transition.called:
                    print(f"Transitioned to new scene in run {i}")
                if mock_quit.called:
                    print(f"Quit game in run {i}")
