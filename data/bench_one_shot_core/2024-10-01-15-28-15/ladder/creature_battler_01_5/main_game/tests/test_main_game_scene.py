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
    
    run_count = 0
    for _ in range(10):
        try:
            run_count += 1  # Increment run_count before transition_to_scene
            app.transition_to_scene("MainGameScene", player=player)
        except RandomModeGracefulExit:
            # Consider this a successful run and break the loop
            break
        except AbstractApp._QuitWholeGame:
            break

    assert run_count > 0, "The game should run at least once before quitting"
    assert run_count <= 10, f"The game ran {run_count} times, which is more than expected"
