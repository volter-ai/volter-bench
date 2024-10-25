import pytest
from main_game.main import App
from main_game.scenes.main_menu_scene import MainMenuScene
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_button
from mini_game_engine.engine.lib import HumanListener


@pytest.fixture
def app():
    return App()

def test_main_menu_scene(app):
    HumanListener.random_mode = True
    player = app.create_player("test_player")
    
    for _ in range(10):
        try:
            app.run(player)
        except HumanListener.RandomModeGracefulExit:
            pass

class TestMainMenuScene:
    def test_play_game(self, app):
        player = app.create_player("test_player")
        scene = MainMenuScene(app, player)

        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        choices = runner.dequeue_wait_for_choice(player)
        play_button = find_button(choices, "Play")
        runner.make_choice(play_button)

        assert runner.dequeue_transition_to_scene() == "MainGameScene"

    def test_quit_game(self, app):
        player = app.create_player("test_player")
        scene = MainMenuScene(app, player)

        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        choices = runner.dequeue_wait_for_choice(player)
        quit_button = find_button(choices, "Quit")
        runner.make_choice(quit_button)

        runner.dequeue_quit_whole_game()
