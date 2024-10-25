import pytest
from mini_game_engine.engine.lib import HumanListener, AbstractApp
from main_game.main import App


@pytest.fixture
def app():
    return App()

def test_main_menu_scene(app):
    HumanListener.random_mode = True
    player = app.create_player("test_player")
    
    for _ in range(10):
        try:
            app.transition_to_scene("MainMenuScene", player=player)
        except AbstractApp._QuitWholeGame:
            # This exception is expected when the game ends gracefully
            break
