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
            HumanListener.random_mode_counter = 30  # More moves needed for complex battle scene

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
                    print(f"Exiting scene via transition in run {i}")
                except AbstractApp._QuitWholeGame:
                    print(f"Exiting scene via quit in run {i}")
                except RandomModeGracefulExit:
                    print(f"Random mode counter reached 0 in run {i}")
                else:
                    assert mock_transition.called or scene._app.terminated
                    if mock_transition.called:
                        print("Exited via transition")
                    if scene._app.terminated:
                        print("Exited via quit")
                finally:
                    mock_transition.reset_mock()
