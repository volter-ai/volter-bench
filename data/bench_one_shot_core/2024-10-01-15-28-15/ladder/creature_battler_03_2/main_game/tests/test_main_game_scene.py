import pytest
from main_game.main import App
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit


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
            pass

    HumanListener.random_mode = False
