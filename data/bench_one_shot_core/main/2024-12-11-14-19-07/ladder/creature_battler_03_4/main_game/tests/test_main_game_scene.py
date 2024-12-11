import pytest
from unittest.mock import patch
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit, AbstractApp

from main_game.scenes.main_game_scene import MainGameScene
from main_game.main import App

class TestMainGameSceneRandomRun:
    @pytest.fixture
    def app(self):
        app = App()
        app.register_scene("MainGameScene", MainGameScene)
        return app

    def test_main_game_scene_random_run(self, app):
        for i in range(10):
            print(f"starting random run iteration {i}")
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 30  # More moves needed for battle

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            # Track if battle happened
            battle_happened = False
            battle_ended = False

            def mock_show_text(player, text):
                nonlocal battle_happened, battle_ended
                if "used" in text and "damage" in text:
                    battle_happened = True
                if "won" in text or "lost" in text:
                    battle_ended = True
                print(text)

            # Patch the scene to prevent infinite transitions
            with patch.object(MainGameScene, '_transition_to_scene') as mock_transition, \
                 patch.object(MainGameScene, '_show_text', side_effect=mock_show_text):
                
                try:
                    main_game_scene.run()
                except RandomModeGracefulExit:
                    print(f"`random_mode_counter` reached 0 and the game did not crash. Ending run {i} gracefully")
                except AbstractApp._QuitWholeGame:
                    print(f"Game quit gracefully in run {i}")
                
                # Assert that battle actually happened
                assert battle_happened, "No battle actions were recorded"
                assert battle_ended, "Battle did not reach an end state"
                assert mock_transition.called, "Scene should transition after battle ends"
