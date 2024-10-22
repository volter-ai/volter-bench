import pytest
from main_game.main import App
from mini_game_engine.engine.lib import (AbstractApp, HumanListener,
                                         RandomModeGracefulExit)


@pytest.fixture
def app():
    return App()

def test_main_game_scene(app):
    HumanListener.random_mode = True
    HumanListener.random_mode_counter = 100
    player = app.create_player("test_player")

    iterations = 0

    def count_iterations(scene_name, **kwargs):
        nonlocal iterations
        iterations += 1
        if scene_name == "MainGameScene":
            raise RandomModeGracefulExit()

    app.transition_to_scene = count_iterations

    try:
        app.run(player)
    except (RandomModeGracefulExit, AbstractApp._QuitWholeGame):
        pass

    assert iterations > 0, "The game should run at least once"
