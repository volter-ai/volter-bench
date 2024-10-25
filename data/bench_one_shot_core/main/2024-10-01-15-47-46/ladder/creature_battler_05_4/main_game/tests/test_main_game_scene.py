import pytest
from mini_game_engine.engine.lib import HumanListener, AbstractApp
from main_game.scenes.main_menu_scene import MainMenuScene
from main_game.scenes.main_game_scene import MainGameScene
from main_game.models import Player


class TestApp(AbstractApp):
    def __init__(self):
        super().__init__()
        self.register_scene("MainMenuScene", MainMenuScene, is_entry_point=True)
        self.register_scene("MainGameScene", MainGameScene)

    def create_player(self, player_id: str):
        player = Player.from_prototype_id(prototype_id="default_player")
        player.uid = player_id
        player.set_listener(HumanListener())
        return player

    def create_bot(self, prototype_id: str):
        return self.create_player(prototype_id)  # For simplicity, create a player instead of a bot

@pytest.fixture
def app():
    return TestApp()

@pytest.fixture
def player(app):
    return app.create_player("test_player")

def test_main_game_scene(app, player):
    HumanListener.random_mode = True
    try:
        for _ in range(10):
            scene = MainGameScene(app, player)
            scene.run()
    except AbstractApp._QuitWholeGame:
        pass  # Expected exception when quitting the game
    finally:
        HumanListener.random_mode = False
