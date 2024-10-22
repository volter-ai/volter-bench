import pytest
from main_game.models import Player
from main_game.scenes.main_game_scene import MainGameScene
from main_game.scenes.main_menu_scene import MainMenuScene
from mini_game_engine.engine.lib import AbstractApp, BotListener, HumanListener
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_button


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
    max_iterations = 100
    iterations = 0
    
    try:
        while iterations < max_iterations:
            scene = MainMenuScene(app, player)
            try:
                scene.run()
            except AbstractApp._QuitWholeGame:
                break  # Exit the loop if the game ends
            iterations += 1
    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {str(e)}")

    assert iterations < max_iterations, "The game did not end within the expected number of iterations"

class TestMainMenuScene:
    def test_player_chooses_play(self, app, player):
        scene = MainMenuScene(app, player)
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        choices = runner.dequeue_wait_for_choice(player)
        play_button = find_button(choices, "Play")
        runner.make_choice(play_button)

        assert runner.dequeue_transition_to_scene() == "MainGameScene"

    def test_player_chooses_quit(self, app, player):
        scene = MainMenuScene(app, player)
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        choices = runner.dequeue_wait_for_choice(player)
        quit_button = find_button(choices, "Quit")
        runner.make_choice(quit_button)

        runner.dequeue_quit_whole_game()
