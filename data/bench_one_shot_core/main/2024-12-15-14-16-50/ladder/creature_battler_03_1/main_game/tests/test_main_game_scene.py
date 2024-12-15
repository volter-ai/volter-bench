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
            HumanListener.random_mode_counter = 30

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            class TransitionFromScene(Exception):
                pass

            def exit_scene(*args, **kwargs):
                raise TransitionFromScene()

            # patch the transition method to catch scene exits
            with patch.object(MainGameScene, '_transition_to_scene', side_effect=exit_scene) as mock_transition:
                try:
                    main_game_scene.run()
                except TransitionFromScene:
                    print(f"Scene exited properly via transition for run {i}")
                    assert mock_transition.called, "Scene should transition at end of battle"
                    assert mock_transition.call_args[0][0] == "MainMenuScene", "Should transition to main menu"
                except RandomModeGracefulExit:
                    print(f"Random mode completed successfully for run {i}")
                except AbstractApp._QuitWholeGame:
                    print(f"Game quit gracefully for run {i}")
                
                # Verify battle ended properly
                assert (main_game_scene.player_creature.hp <= 0 or 
                       main_game_scene.opponent_creature.hp <= 0), "Battle should end with a winner"
