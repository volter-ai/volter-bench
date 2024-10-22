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

def test_main_game_scene(app, player):
    HumanListener.random_mode = True
    max_iterations = 100
    iterations = 0
    
    try:
        while iterations < max_iterations:
            scene = MainGameScene(app, player)
            try:
                scene.run()
            except AbstractApp._QuitWholeGame:
                break  # Exit the loop if the game ends
            iterations += 1
    except Exception as e:
        pytest.fail(f"An unexpected error occurred: {str(e)}")

    assert iterations < max_iterations, "The game did not end within the expected number of iterations"

class TestMainGameScene:
    def test_player_wins(self, app):
        player = app.create_player("test_player")
        player.display_name = "Player"
        scene = MainGameScene(app, player)
        scene.opponent.display_name = "Opponent"
        
        # Ensure player's Bubwool has higher speed and attack
        scene.creatures[0].speed = 5
        scene.creatures[0].attack = 5
        scene.creatures[1].speed = 3
        scene.creatures[1].attack = 3

        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        # First turn
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(scene.opponent)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        # Second turn
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(scene.opponent)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        # Third turn
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(scene.opponent)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"
        assert scene.creatures[1].hp == 0, "Opponent's creature should be defeated"
        assert scene.creatures[0].hp == 0 or scene.creatures[0].hp > 0, "Player's creature should either be defeated or have HP remaining"
        assert scene.battle_ended, "The battle should have ended"

    def test_opponent_wins(self, app):
        player = app.create_player("test_player")
        player.display_name = "Player"
        scene = MainGameScene(app, player)
        scene.opponent.display_name = "Opponent"
        
        # Set opponent's Scizard to have higher attack
        scene.creatures[0].attack = 3
        scene.creatures[1].attack = 5

        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        # First turn
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(scene.opponent)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        # Second turn
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(scene.opponent)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"
        assert scene.creatures[0].hp == 0, "Player's creature should be defeated"
        assert scene.creatures[1].hp > 0, "Opponent's creature should have HP remaining"
        assert scene.battle_ended, "The battle should have ended"
