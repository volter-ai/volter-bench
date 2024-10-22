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
    
    completed_games = 0
    max_attempts = 10

    for _ in range(max_attempts):
        try:
            app.transition_to_scene("MainGameScene", player=player)
        except AbstractApp._QuitWholeGame:
            # This exception indicates a successful game completion
            completed_games += 1
        except RandomModeGracefulExit:
            # This exception is expected and should be ignored
            pass

        if completed_games > 0:
            break  # We've successfully completed at least one game

    HumanListener.random_mode = False

    assert completed_games > 0, f"Failed to complete any games in {max_attempts} attempts"
