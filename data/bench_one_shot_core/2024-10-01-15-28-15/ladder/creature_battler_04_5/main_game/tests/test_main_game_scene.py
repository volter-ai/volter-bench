import pytest
from mini_game_engine.engine.lib import (AbstractApp, AbstractGameEntity,
                                         HumanListener, RandomModeGracefulExit)


class BattleCompletedEvent(AbstractGameEntity):
    pass

@pytest.fixture
def app():
    from main_game.main import App
    return App()

def test_main_game_scene(app):
    HumanListener.random_mode = True
    player = app.create_player("test_player")
    
    battles_completed = 0
    max_battles = 10
    min_battles = 3

    def on_battle_completed(event):
        nonlocal battles_completed
        if isinstance(event, BattleCompletedEvent):
            battles_completed += 1

    AbstractApp.subscribe_to_events(on_battle_completed)

    try:
        app.transition_to_scene("MainGameScene", player=player)
    except (RandomModeGracefulExit, AbstractApp._QuitWholeGame):
        pass

    AbstractApp.unsubscribe_from_events(on_battle_completed)

    assert battles_completed >= min_battles, f"Game ended too quickly. Only completed {battles_completed} battles, expected at least {min_battles}."

    HumanListener.random_mode = False
