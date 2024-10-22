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

            class BattleEnded(Exception):
                pass

            def end_battle(*args, **kwargs):
                raise BattleEnded()

            with patch.object(MainGameScene, 'check_battle_end', side_effect=end_battle) as mock_battle_end:
                try:
                    main_game_scene.run()
                except BattleEnded:
                    print(f"Battle ended, so ending run {i}")
                except RandomModeGracefulExit:
                    print(f"`random_mode_counter` reached 0 and the game did not crash. Ending run {i} gracefully")
                else:
                    assert False, "Battle did not end as expected"
                finally:
                    mock_battle_end.reset_mock()
