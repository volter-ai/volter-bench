import pytest
from main_game.models import Player
from main_game.scenes.main_game_scene import MainGameScene
from main_game.scenes.main_menu_scene import MainMenuScene
from mini_game_engine.engine.lib import (AbstractApp, HumanListener,
                                         RandomModeGracefulExit)


class TestApp(AbstractApp):
    def __init__(self):
        super().__init__()
        self.register_scene("MainGameScene", MainGameScene)
        self.register_scene("MainMenuScene", MainMenuScene)

    def create_player(self, player_id: str):
        player = Player.from_prototype_id(prototype_id="default_player")
        player.uid = player_id
        player.set_listener(HumanListener())
        return player

    def create_bot(self, prototype_id: str):
        return self.create_player(prototype_id)  # For simplicity, create a player instead of a bot

    def quit_whole_game(self):
        # Instead of raising an exception, we'll just pass
        pass

@pytest.fixture
def app():
    return TestApp()

@pytest.fixture
def player(app):
    return app.create_player("test_player")

def test_main_game_scene(app, player):
    HumanListener.random_mode = True
    HumanListener.random_mode_counter = 100  # Reset the counter for each test
    for _ in range(10):
        scene = MainGameScene(app, player)
        try:
            scene.run()
        except (RandomModeGracefulExit, AbstractApp._QuitWholeGame):
            # These exceptions are expected in random mode, so we'll just continue
            continue
    HumanListener.random_mode = False
