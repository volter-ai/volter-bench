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
            HumanListener.random_mode_counter = 30  # Need more moves for battle scene

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            class TransitionFromScene(Exception):
                pass

            def exit_scene(*args, **kwargs):
                raise TransitionFromScene()

            # Mock the transition to prevent scene cycling
            with patch.object(MainGameScene, '_transition_to_scene', side_effect=exit_scene):
                try:
                    main_game_scene.run()
                except (RandomModeGracefulExit, TransitionFromScene):
                    print(f"Scene completed successfully in run {i}")
                except AbstractApp._QuitWholeGame:
                    print(f"Game quit gracefully in run {i}")
