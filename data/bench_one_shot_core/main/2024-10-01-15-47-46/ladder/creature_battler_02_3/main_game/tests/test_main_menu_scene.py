import pytest
from mini_game_engine.engine.lib import AbstractApp, HumanListener, BotListener
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_button
from main_game.scenes.main_menu_scene import MainMenuScene
from main_game.scenes.main_game_scene import MainGameScene
from main_game.models import Player
from mini_game_engine.engine.lib import RandomModeGracefulExit


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

def test_main_menu_scene(app, player):
    HumanListener.random_mode = True
    HumanListener.random_mode_counter = 1000  # Increase the counter to allow for more interactions

    scene = MainMenuScene(app, player)
    
    try:
        scene.run()
    except (AbstractApp._QuitWholeGame, RandomModeGracefulExit):
        # These exceptions are expected when the game ends or random mode finishes
        pass
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

    # If we reach this point without any unexpected exceptions, the test is considered successful
    assert True

def test_main_menu_scene_play(app, player):
    scene = MainMenuScene(app, player)
    runner = ThreadedSceneRunner()
    runner.start_game(scene)

    choices = runner.dequeue_wait_for_choice(player)
    play_button = find_button(choices, "Play")
    runner.make_choice(play_button)

    assert runner.dequeue_transition_to_scene() == "MainGameScene"

def test_main_menu_scene_quit(app, player):
    scene = MainMenuScene(app, player)
    runner = ThreadedSceneRunner()
    runner.start_game(scene)

    choices = runner.dequeue_wait_for_choice(player)
    quit_button = find_button(choices, "Quit")
    runner.make_choice(quit_button)

    runner.dequeue_quit_whole_game()
