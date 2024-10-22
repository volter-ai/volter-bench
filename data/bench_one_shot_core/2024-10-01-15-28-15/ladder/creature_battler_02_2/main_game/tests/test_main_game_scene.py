import pytest
from main_game.models import Player
from main_game.scenes.main_game_scene import MainGameScene
from main_game.scenes.main_menu_scene import MainMenuScene
from mini_game_engine.engine.lib import (AbstractApp, BotListener,
                                         HumanListener, RandomModeGracefulExit)


class TestApp(AbstractApp):
    def __init__(self):
        super().__init__()
        self.register_scene("MainMenuScene", MainMenuScene)
        self.register_scene("MainGameScene", MainGameScene)

    def create_player(self, player_id: str) -> Player:
        player = Player.from_prototype_id("default_player")
        player.uid = player_id
        player.set_listener(HumanListener())
        return player

    def create_bot(self, prototype_id: str) -> Player:
        bot = Player.from_prototype_id(prototype_id)
        bot.set_listener(BotListener())
        return bot

@pytest.fixture
def app():
    return TestApp()

@pytest.fixture
def player(app):
    return app.create_player("test_player")

def test_main_game_scene(app, player):
    HumanListener.random_mode = True
    HumanListener.random_mode_counter = 100  # Set a high enough value to ensure the game completes

    scene = MainGameScene(app, player)
    game_ended_normally = False

    try:
        scene.run()
    except (RandomModeGracefulExit, AbstractApp._QuitWholeGame):
        # Either of these exceptions indicates the game ended normally
        game_ended_normally = True
    except Exception as e:
        pytest.fail(f"Unexpected exception occurred: {e}")

    assert game_ended_normally, "The game did not end as expected"
