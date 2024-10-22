import pytest
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit, AbstractApp
from main_game.main import App


@pytest.fixture
def app():
    return App()

def test_main_game_scene(app):
    HumanListener.random_mode = True
    player = app.create_player("test_player")
    
    for _ in range(10):
        try:
            app.transition_to_scene("MainGameScene", player=player)
        except RandomModeGracefulExit:
            break
        except AbstractApp._QuitWholeGame:
            # This exception indicates a successful game completion
            break

    HumanListener.random_mode = False
