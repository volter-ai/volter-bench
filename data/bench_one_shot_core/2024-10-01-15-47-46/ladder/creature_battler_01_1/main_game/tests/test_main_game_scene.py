import pytest
from main_game.main import App
from main_game.models import Creature
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.lib import AbstractApp, HumanListener
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_button


@pytest.fixture
def app():
    return App()

def test_main_game_scene(app):
    HumanListener.random_mode = True
    player = app.create_player("test_player")
    
    for _ in range(10):
        try:
            app.transition_to_scene("MainGameScene", player=player)
        except AbstractApp._QuitWholeGame:
            # This is the expected behavior when the game ends
            break

    # Reset the random mode after the test
    HumanListener.random_mode = False

class TestMainGameScene:
    @pytest.fixture
    def player(self, app):
        player = app.create_player("test_player")
        player.display_name = "Player 1"
        return player

    @pytest.fixture
    def opponent(self, app):
        opponent = app.create_bot("default_player")
        opponent.display_name = "Player 2"
        return opponent

    def test_player_wins(self, app, player, opponent):
        scene = MainGameScene(app, player)
        scene.opponent = opponent
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        for _ in range(4):
            choices = runner.dequeue_wait_for_choice(player)
            tackle = find_button(choices, "Tackle")
            runner.make_choice(tackle)

            choices = runner.dequeue_wait_for_choice(opponent)
            tackle = find_button(choices, "Tackle")
            runner.make_choice(tackle)

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"

    def test_player_loses(self, app, player, opponent):
        weak_creature = Creature.from_prototype_id("bubwool")
        weak_creature.hp = 1
        weak_creature.max_hp = 1
        player.creatures = [weak_creature]

        scene = MainGameScene(app, player)
        scene.opponent = opponent
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(opponent)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"

    def test_player_quits(self, app, player, opponent):
        scene = MainGameScene(app, player)
        scene.opponent = opponent
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        choices = runner.dequeue_wait_for_choice(player)
        quit_button = find_button(choices, "Quit")
        runner.make_choice(quit_button)

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"
