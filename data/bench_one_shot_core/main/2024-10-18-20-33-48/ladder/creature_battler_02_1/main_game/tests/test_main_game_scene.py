import pytest
from unittest.mock import patch
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene


class TestMainGameSceneRandomRun:
    @pytest.fixture
    def app(self):
        return App()

    def test_main_game_scene_random_run(self, app):
        for i in range(10):
            print(f"starting random run iteration {i}")
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 30  # Increased to 30 for more complex scene

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            class BattleEnd(Exception):
                pass

            def exit_scene(*args, **kwargs):
                raise BattleEnd()

            with patch.object(MainGameScene, '_transition_to_scene', side_effect=exit_scene) as mock_transition, \
                    patch.object(MainGameScene, '_quit_whole_game') as mock_quit:

                try:
                    main_game_scene.run()
                except BattleEnd:
                    print(f"Battle ended, exiting MainGameScene so ending run {i}")
                except RandomModeGracefulExit:
                    print(f"`random_mode_counter` reached 0 and the game did not crash. Ending run {i} gracefully")
                else:
                    assert mock_transition.called or mock_quit.called, "scene was not exited in an expected manner"

                    if mock_quit.called:
                        print("_quit_whole_game called")
                    if mock_transition.called:
                        print("_transition_to_scene called")
                finally:
                    mock_transition.reset_mock()
                    mock_quit.reset_mock()
