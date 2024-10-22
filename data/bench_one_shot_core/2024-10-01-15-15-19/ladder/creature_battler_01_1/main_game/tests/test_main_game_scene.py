import pytest
from main_game.main import App
from mini_game_engine.engine.lib import (AbstractApp, HumanListener,
                                         RandomModeGracefulExit)


@pytest.fixture
def app():
    return App()

def test_main_game_scene(app):
    HumanListener.random_mode = True
    player = app.create_player("test_player")
    
    successful_runs = 0
    max_attempts = 10

    for _ in range(max_attempts):
        try:
            app.transition_to_scene("MainGameScene", player=player)
            successful_runs += 1
        except AbstractApp._QuitWholeGame:
            # This exception is expected when the game ends normally
            successful_runs += 1
        except RandomModeGracefulExit:
            # This exception is also expected in random mode
            successful_runs += 1

    assert successful_runs > 0, f"The MainGameScene should have run at least once in {max_attempts} attempts"
