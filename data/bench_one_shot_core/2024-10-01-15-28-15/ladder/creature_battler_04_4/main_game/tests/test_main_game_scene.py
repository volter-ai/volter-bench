import pytest
from mini_game_engine.engine.lib import (AbstractApp, HumanListener,
                                         RandomModeGracefulExit)

# Add this method to the AbstractGameScene class in mini_game_engine/engine/lib.py
# def get_battles_played(self):
#     return getattr(self, 'battles_played', 0)

@pytest.fixture
def app():
    from main_game.main import App
    return App()

def test_main_game_scene(app):
    HumanListener.random_mode = True
    player = app.create_player("test_player")
    
    min_battles = 3
    max_attempts = 10

    for _ in range(max_attempts):
        try:
            scene = app.transition_to_scene("MainGameScene", player=player)
            battles_played = scene.get_battles_played()
            assert battles_played >= min_battles, f"Game ended too quickly. Only played {battles_played} battles, expected at least {min_battles}."
            break
        except (RandomModeGracefulExit, AbstractApp._QuitWholeGame):
            continue
    else:
        pytest.fail(f"Game did not complete {min_battles} battles in {max_attempts} attempts.")

    HumanListener.random_mode = False
