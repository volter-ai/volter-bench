import pytest
from main_game.models import Player
from main_game.scenes.main_menu_scene import MainMenuScene
from mini_game_engine.engine.lib import (AbstractApp, AbstractGameScene,
                                         HumanListener)


class DummyMainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)

    def __str__(self):
        return "Dummy Main Game Scene"

    def run(self):
        self._show_text(self.player, "This is a dummy game scene.")
        self._transition_to_scene("MainMenuScene")  # Add this line to transition back to MainMenuScene

class TestApp(AbstractApp):
    def __init__(self):
        super().__init__()
        self.register_scene("MainMenuScene", MainMenuScene, is_entry_point=True)
        self.register_scene("MainGameScene", DummyMainGameScene)

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

def test_main_menu_scene(app, player):
    HumanListener.random_mode = True
    for _ in range(10):
        scene = MainMenuScene(app, player)
        scene.run()
    HumanListener.random_mode = False
