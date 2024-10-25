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
        HumanListener.random_mode_counter = 100  # Reset the counter before each run
        try:
            app.transition_to_scene("MainGameScene", player=player)
        except (RandomModeGracefulExit, AbstractApp._QuitWholeGame):
            # These exceptions are expected when the random mode counter reaches zero
            # or when the game ends gracefully
            pass
