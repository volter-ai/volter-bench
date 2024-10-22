import pytest
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene


@pytest.fixture
def app():
    return App()

def test_main_game_scene(app):
    HumanListener.random_mode = True
    player = app.create_player("test_player")
    
    for _ in range(10):
        try:
            scene = MainGameScene(app, player)
            scene.run()
        except RandomModeGracefulExit:
            pass

    HumanListener.random_mode = False
