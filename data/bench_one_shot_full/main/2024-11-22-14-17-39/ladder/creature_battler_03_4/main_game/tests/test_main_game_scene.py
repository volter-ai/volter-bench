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
            HumanListener.random_mode_counter = 30  # More moves needed for battle scene

            player = app.create_player(f"player_{i}")
            scene = MainGameScene(app, player)

            # Mock transition to prevent infinite loop
            with patch.object(MainGameScene, '_transition_to_scene') as mock_transition:
                try:
                    scene.run()
                except RandomModeGracefulExit:
                    print(f"random mode counter reached 0")
                except AbstractApp._QuitWholeGame:
                    print(f"game quit gracefully")
                
                # Verify the scene tried to transition back to menu at least once
                assert mock_transition.called
                assert mock_transition.call_args[0][0] == "MainMenuScene"
                
                # Verify battle ended (either player or opponent should be at 0 HP)
                assert scene.player_creature.hp <= 0 or scene.opponent_creature.hp <= 0
