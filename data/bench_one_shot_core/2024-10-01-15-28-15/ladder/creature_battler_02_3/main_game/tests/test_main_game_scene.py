import pytest
from mini_game_engine.engine.lib import HumanListener, AbstractApp, BotListener, RandomModeGracefulExit
from main_game.scenes.main_game_scene import MainGameScene
from main_game.scenes.main_menu_scene import MainMenuScene
from main_game.models import Player


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
    HumanListener.random_mode_counter = 100  # Set a high enough value to complete the game

    scene = MainGameScene(app, player)
    game_completed = False

    try:
        scene.run()
    except (RandomModeGracefulExit, AbstractApp._QuitWholeGame):
        # Either of these exceptions indicates the game has completed
        game_completed = True
    except Exception as e:
        pytest.fail(f"Unexpected exception occurred: {e}")

    assert game_completed, "The game did not complete as expected"
