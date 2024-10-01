import pytest
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit, AbstractApp
from main_game.main import App


@pytest.fixture
def app():
    return App()

def test_main_game_scene(app):
    HumanListener.random_mode = True
    player = app.create_player("test_player")
    
    run_count = 0
    for _ in range(10):
        HumanListener.random_mode_counter = 100  # Reset the counter before each run
        try:
            app.transition_to_scene("MainGameScene", player=player)
            run_count += 1
        except AbstractApp._QuitWholeGame:
            break  # Game ended as expected
        except RandomModeGracefulExit:
            continue  # Random mode ended, but we want to try again

    assert run_count > 0, "The MainGameScene should run at least once"
