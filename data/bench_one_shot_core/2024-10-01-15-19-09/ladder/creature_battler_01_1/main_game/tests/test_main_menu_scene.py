import pytest
from main_game.main import App
from mini_game_engine.engine.lib import (AbstractApp, HumanListener,
                                         RandomModeGracefulExit)


@pytest.fixture
def app():
    return App()

def test_main_menu_scene(app):
    HumanListener.random_mode = True
    player = app.create_player("test_player")
    
    run_count = 0
    max_runs = 10

    try:
        for _ in range(max_runs):
            try:
                app.transition_to_scene("MainMenuScene", player=player)
                run_count += 1
            except RandomModeGracefulExit:
                run_count += 1
                break
    except AbstractApp._QuitWholeGame:
        pass

    HumanListener.random_mode = False
    assert run_count > 0, f"MainMenuScene should run at least once, but ran {run_count} times"
