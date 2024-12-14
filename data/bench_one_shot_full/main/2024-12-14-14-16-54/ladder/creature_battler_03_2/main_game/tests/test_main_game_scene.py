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

            # Patch both transition and quit methods to catch either exit path
            with patch.object(MainGameScene, '_transition_to_scene', side_effect=exit_scene) as mock_transition, \
                 patch.object(MainGameScene, '_quit_whole_game') as mock_quit:

                try:
                    main_game_scene.run()
                except TransitionFromScene:
                    print(f"Scene transitioned as expected in run {i}")
                    assert mock_transition.called, "Scene should transition at end of battle"
                    assert mock_transition.call_args[0][0] == "MainMenuScene", "Should transition to main menu"
                except RandomModeGracefulExit:
                    print(f"Random mode counter reached 0 in run {i}")
                except AbstractApp._QuitWholeGame:
                    print(f"Game quit gracefully in run {i}")
                    assert mock_quit.called, "Game should quit cleanly"
                
                # Verify battle ended one way or another
                assert (mock_transition.called or mock_quit.called), \
                    "Scene should either transition or quit"

                # Reset mocks for next iteration
                mock_transition.reset_mock()
                mock_quit.reset_mock()
