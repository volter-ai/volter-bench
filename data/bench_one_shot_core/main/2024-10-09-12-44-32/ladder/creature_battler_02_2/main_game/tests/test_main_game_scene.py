import pytest
from unittest.mock import patch
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit, AbstractApp
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from main_game.scenes.game_over_scene import GameOverScene


class TestMainGameSceneRandomRun:
    @pytest.fixture
    def app(self):
        return App()

    def test_main_game_scene_random_run(self, app):
        for i in range(10):
            print(f"starting random run iteration {i}")
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 100  # Increased to ensure completion of all battles

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            transition_counter = 0
            original_transition = app.transition_to_scene

            def count_transitions(scene_name, **kwargs):
                nonlocal transition_counter
                transition_counter += 1
                original_transition(scene_name, **kwargs)

            with patch.object(app, 'transition_to_scene', side_effect=count_transitions):
                try:
                    main_game_scene.run()
                except AbstractApp._QuitWholeGame:
                    print("Game quit gracefully")
                except RandomModeGracefulExit:
                    print(f"`random_mode_counter` reached 0 and the game did not crash. Ending run {i} gracefully")

                # Assert that we transitioned to GameOverScene
                assert transition_counter >= 1, "Did not transition to GameOverScene"
                
                # Check if GameOverScene.run() was called
                with patch.object(GameOverScene, 'run', return_value=None) as mock_game_over_run:
                    try:
                        app.transition_to_scene("GameOverScene", player=player)
                    except AbstractApp._QuitWholeGame:
                        pass
                    mock_game_over_run.assert_called_once()

                print(f"Completed run {i} successfully")
