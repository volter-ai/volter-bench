import pytest
from mini_game_engine.engine.lib import HumanListener, AbstractApp
from main_game.main import App


@pytest.fixture
def app():
    return App()

@pytest.fixture
def player(app):
    return app.create_player("test_player")

def reset_creatures(player):
    for creature in player.creatures:
        creature.hp = creature.max_hp

def test_main_game_scene(app, player):
    HumanListener.random_mode = True
    min_turns = 5
    for _ in range(10):
        scene = app.scene_registry["MainGameScene"](app, player)
        game_ended = False
        while scene.turn_count < min_turns and not game_ended:
            try:
                game_ended = scene.run()
            except AbstractApp._QuitWholeGame:
                break
        assert scene.turn_count >= min_turns or game_ended, f"Game ended too quickly after {scene.turn_count} turns"
        reset_creatures(player)
    HumanListener.random_mode = False
