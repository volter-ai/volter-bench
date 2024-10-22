import pytest
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit, AbstractApp
from main_game.main import App


@pytest.fixture
def app():
    return App()

def test_main_menu_scene(app):
    HumanListener.random_mode = True
    HumanListener.random_mode_counter = 100
    player = app.create_player("test_player")

    iterations = 0

    def count_iterations(scene_name, **kwargs):
        nonlocal iterations
        iterations += 1
        if iterations > 1:  # Allow transitioning to MainGameScene once
            raise RandomModeGracefulExit()

    app.transition_to_scene = count_iterations

    try:
        app.run(player)
    except (RandomModeGracefulExit, AbstractApp._QuitWholeGame):
        pass

    assert iterations > 0, "The game should run at least once"
