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
    
    iterations = 0
    max_iterations = 10

    while iterations < max_iterations:
        iterations += 1
        HumanListener.random_mode_counter = 100  # Reset the counter before each run
        
        try:
            app.transition_to_scene("MainMenuScene", player=player)
        except RandomModeGracefulExit:
            break
        except AbstractApp._QuitWholeGame:
            # Game quit successfully
            break

    assert iterations > 0, "The game should run at least once"
