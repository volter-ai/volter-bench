import pytest
from mini_game_engine.engine.lib import AbstractApp, HumanListener
from main_game.models import Player
from main_game.scenes.main_game_scene import MainGameScene
from main_game.scenes.main_menu_scene import MainMenuScene


class TestApp(AbstractApp):
    def __init__(self):
        super().__init__()
        self.register_scene("MainMenuScene", MainMenuScene)
        self.register_scene("MainGameScene", MainGameScene)

    def create_player(self, player_id: str) -> Player:
        player = Player.from_prototype_id(prototype_id="default_player")
        player.uid = player_id
        player.set_listener(HumanListener())
        return player

    def create_bot(self, prototype_id: str) -> Player:
        bot = Player.from_prototype_id(prototype_id=prototype_id)
        bot.uid = "test_bot"
        bot.set_listener(HumanListener())  # Using HumanListener for predictability in tests
        return bot

@pytest.fixture
def app():
    return TestApp()

@pytest.fixture
def player(app):
    return app.create_player("test_player")

def test_main_game_scene(app, player):
    HumanListener.random_mode = True
    game_ended = False
    try:
        for _ in range(10):
            scene = MainGameScene(app, player)
            scene.run()
            game_ended = True
    except AbstractApp._QuitWholeGame:
        pass  # This exception is expected when quitting the game
    finally:
        HumanListener.random_mode = False
    
    assert game_ended, "The game should have run at least once before quitting"
