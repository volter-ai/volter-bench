import pytest
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit, AbstractApp
from main_game.main import App


@pytest.fixture
def app():
    return App()

def test_main_game_scene(app):
    HumanListener.random_mode = True
    player = app.create_player("test_player")
    
    scene_ran = False
    try:
        for _ in range(10):
            try:
                app.transition_to_scene("MainGameScene", player=player)
                scene_ran = True
            except RandomModeGracefulExit:
                pass
    except AbstractApp._QuitWholeGame:
        pass  # Game quit is expected behavior

    assert scene_ran, "The MainGameScene should run at least once"
