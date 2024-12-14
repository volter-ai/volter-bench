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
            print(f"Starting random run iteration {i}")
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 30  # More moves needed for battle scene

            player = app.create_player(f"player_{i}")
            scene = MainGameScene(app, player)

            class TransitionFromScene(Exception):
                pass

            def exit_scene(*args, **kwargs):
                raise TransitionFromScene()

            with patch.object(MainGameScene, '_transition_to_scene', side_effect=exit_scene) as mock_transition:
                try:
                    scene.run()
                except TransitionFromScene:
                    print(f"Scene exited via transition in run {i}")
                except RandomModeGracefulExit:
                    print(f"Random mode counter reached 0 in run {i}")
                except AbstractApp._QuitWholeGame:
                    print(f"Game quit gracefully in run {i}")
                else:
                    assert mock_transition.called, "Scene should have transitioned"
                    print(f"Scene completed normally in run {i}")
