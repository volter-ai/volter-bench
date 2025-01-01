import pytest
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit, AbstractApp
from main_game.main import App
from main_game.scenes.main_menu_scene import MainMenuScene

@pytest.fixture
def app():
    return App()

def test_main_menu_scene_random_run(app):
    HumanListener.random_mode = True
    HumanListener.random_mode_counter = 10

    player = app.create_player("test_player")
    scene = MainMenuScene(app, player)

    try:
        scene.run()
    except (RandomModeGracefulExit, AbstractApp._QuitWholeGame):
        # Catch the expected exceptions to allow the test to pass
        pass
