import pytest
from unittest.mock import patch

from mini_game_engine.engine.lib import (
    HumanListener, 
    RandomModeGracefulExit, 
    AbstractApp,
    AbstractGameScene
)
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

            # Patch transition_to_scene to prevent actual transitions during test
            with patch.object(AbstractGameScene, '_transition_to_scene') as mock_transition:
                try:
                    main_game_scene.run()
                except (RandomModeGracefulExit, AbstractApp._QuitWholeGame) as e:
                    print(f"Run {i} ended gracefully with: {str(e)}")
                    # Either exception is valid - the scene ended properly
                    continue
                else:
                    # Make sure we either transitioned or hit the random mode limit
                    assert mock_transition.called or HumanListener.random_mode_counter <= 0, \
                        "Scene ended without transition or reaching random mode limit"
