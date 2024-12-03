import pytest
from unittest.mock import patch
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit
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
            HumanListener.random_mode_counter = 30  # More moves needed for complex battle scene

            player = app.create_player(f"player_{i}")
            scene = MainGameScene(app, player)

            class TransitionFromScene(Exception):
                pass

            def exit_scene(*args, **kwargs):
                raise TransitionFromScene()

            with patch.object(MainGameScene, '_transition_to_scene', side_effect=exit_scene) as mock_transition, \
                 patch.object(MainGameScene, '_quit_whole_game') as mock_quit:

                try:
                    scene.run()
                except TransitionFromScene:
                    print(f"exiting scene via transition")
                except RandomModeGracefulExit:
                    print(f"random mode counter reached 0")
                else:
                    assert mock_transition.called or mock_quit.called, "Scene did not exit properly"
                    
                    # Verify battle ended properly
                    player_has_creatures = any(c.hp > 0 for c in player.creatures)
                    bot_has_creatures = any(c.hp > 0 for c in scene.bot.creatures)
                    assert not (player_has_creatures and bot_has_creatures), "Battle ended without a winner"
                finally:
                    mock_transition.reset_mock()
                    mock_quit.reset_mock()
