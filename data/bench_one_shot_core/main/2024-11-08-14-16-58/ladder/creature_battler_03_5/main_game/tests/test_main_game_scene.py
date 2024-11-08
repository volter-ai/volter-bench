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
            HumanListener.random_mode_counter = 30

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            class TransitionFromScene(Exception):
                pass

            def exit_scene(*args, **kwargs):
                raise TransitionFromScene()

            # Patch transition_to_scene to prevent infinite scene transitions
            with patch.object(MainGameScene, '_transition_to_scene', side_effect=exit_scene):
                try:
                    main_game_scene.run()
                except (RandomModeGracefulExit, AbstractApp._QuitWholeGame, TransitionFromScene):
                    # Any of these exceptions indicates a valid end to the scene
                    print(f"Scene ended normally in run {i}")
                    continue
                except Exception as e:
                    # Any other exception is a real error
                    raise e
