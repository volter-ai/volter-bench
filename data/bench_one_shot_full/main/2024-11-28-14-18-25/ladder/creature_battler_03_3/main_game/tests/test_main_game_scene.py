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

            # Patch the transition to prevent infinite scene loops
            with patch.object(MainGameScene, '_transition_to_scene', side_effect=exit_scene):
                try:
                    main_game_scene.run()
                except (RandomModeGracefulExit, AbstractApp._QuitWholeGame):
                    print(f"Random mode counter reached 0 or game quit. Ending run {i}")
                except TransitionFromScene:
                    print(f"Scene transitioned successfully. Ending run {i}")
                else:
                    raise AssertionError("Scene did not end in an expected way")
