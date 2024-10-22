import pytest
from mini_game_engine.engine.lib import HumanListener, AbstractApp, BotListener, RandomModeGracefulExit
from main_game.scenes.main_menu_scene import MainMenuScene
from main_game.scenes.main_game_scene import MainGameScene
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
        bot.uid = f"bot_{prototype_id}"
        bot.set_listener(BotListener())
        return bot

@pytest.fixture
def app():
    return TestApp()

@pytest.fixture
def player(app):
    return app.create_player("test_player")

def test_main_menu_scene(app, player):
    HumanListener.random_mode = True
    max_iterations = 3
    max_choices = 50

    for _ in range(max_iterations):
        scene = MainMenuScene(app, player)
        HumanListener.random_mode_counter = max_choices

        try:
            scene.run()
        except RandomModeGracefulExit:
            # This exception is expected when the random mode ends
            pass
        except AbstractApp._QuitWholeGame:
            # This exception is expected when the game ends
            pass
        except Exception as e:
            pytest.fail(f"Unexpected exception: {e}")

    # If we've completed all iterations without any unexpected exceptions, the test passes
    assert True
