import pytest
from main_game.main import App
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit


@pytest.fixture
def app():
    return App()

def test_main_menu_scene(app):
    HumanListener.random_mode = True
    player = app.create_player("test_player")
    
    for _ in range(10):
        try:
            app.run(player)
        except RandomModeGracefulExit:
            pass

    HumanListener.random_mode = False
