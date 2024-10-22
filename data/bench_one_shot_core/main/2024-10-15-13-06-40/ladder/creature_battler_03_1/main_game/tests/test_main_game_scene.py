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
            opponent = app.create_bot("basic_opponent")
            main_game_scene = MainGameScene(app, player)
            main_game_scene.opponent = opponent

            class BattleEnd(Exception):
                pass

            def exit_scene(*args, **kwargs):
                raise BattleEnd()

            with patch.object(MainGameScene, '_show_text', side_effect=exit_scene) as mock_show_text:
                try:
                    main_game_scene.run()
                except BattleEnd:
                    print(f"Battle ended, exiting MainGameScene for run {i}")
                except RandomModeGracefulExit:
                    print(f"`random_mode_counter` reached 0 and the game did not crash. Ending run {i} gracefully")
                else:
                    assert mock_show_text.called, "Battle did not end as expected"
                    print("Battle ended normally")
                finally:
                    mock_show_text.reset_mock()
