import pytest
from mini_game_engine.engine.lib import HumanListener
from main_game.main import App


@pytest.fixture
def app():
    return App()

@pytest.fixture
def player(app):
    return app.create_player("test_player")

def test_main_menu_scene(app, player):
    HumanListener.random_mode = True
    for _ in range(10):
        scene = app.scene_registry["MainMenuScene"](app, player)
        try:
            scene.run()
        except App._QuitWholeGame:
            pass
    HumanListener.random_mode = False
