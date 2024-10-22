import pytest
from mini_game_engine.engine.lib import (AbstractApp, AbstractPlayerListener,
                                         HumanListener, RandomModeGracefulExit)


class TestListener(AbstractPlayerListener):
    def __init__(self):
        self.battle_count = 0

    def on_wait_for_choice(self, scene, choices):
        return choices[0]

    def on_show_event(self, event_type, event_data):
        if event_type == "battle_completed":
            self.battle_count += 1

    def on_show_scene(self, scene_name, view_data):
        pass

    def on_go_to_single_player_scene(self, app, scene_name):
        pass

@pytest.fixture
def app():
    from main_game.main import App
    return App()

def test_main_game_scene(app):
    HumanListener.random_mode = True
    player = app.create_player("test_player")
    test_listener = TestListener()
    player.set_listener(test_listener)

    max_iterations = 10
    min_battles = 3

    try:
        app.transition_to_scene("MainGameScene", player=player)
    except (RandomModeGracefulExit, AbstractApp._QuitWholeGame):
        pass

    assert test_listener.battle_count >= min_battles, f"Game ended too quickly. Only played {test_listener.battle_count} battles, expected at least {min_battles}."

    HumanListener.random_mode = False
