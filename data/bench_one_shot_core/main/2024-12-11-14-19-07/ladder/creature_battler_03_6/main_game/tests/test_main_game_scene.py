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

            class TransitionFromScene(Exception):
                pass

            def exit_scene(*args, **kwargs):
                raise TransitionFromScene()

            try:
                with patch.object(MainGameScene, '_transition_to_scene', side_effect=exit_scene) as mock_transition:
                    main_game_scene.run()
            except TransitionFromScene:
                print(f"exiting target scene `MainGameScene` so ending run {i}")
            except RandomModeGracefulExit:
                print(f"`random_mode_counter` reached 0 and the game did not crash. Ending run {i} gracefully")
            except AbstractApp._QuitWholeGame:
                print(f"Game quit gracefully via MainMenuScene in run {i}")
            else:
                assert mock_transition.called, "scene was not exited in an expected manner"
            finally:
                mock_transition.reset_mock()
