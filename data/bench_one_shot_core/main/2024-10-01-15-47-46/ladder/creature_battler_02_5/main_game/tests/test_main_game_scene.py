import pytest
from mini_game_engine.engine.lib import AbstractApp, HumanListener, BotListener
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_button
from main_game.scenes.main_game_scene import MainGameScene
from main_game.scenes.main_menu_scene import MainMenuScene
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

def test_main_game_scene(app, player):
    HumanListener.random_mode = True
    HumanListener.random_mode_counter = 100  # Set a high counter to ensure we don't exit prematurely

    scene = MainGameScene(app, player)
    battle_occurred = False

    try:
        scene.run()
    except (RandomModeGracefulExit, AbstractApp._QuitWholeGame):
        # These exceptions are expected when the game ends
        pass
    except Exception as e:
        pytest.fail(f"Unexpected exception occurred: {e}")

    # Check if at least one battle has occurred
    assert player.creatures[0].hp < player.creatures[0].max_hp or \
           scene.opponent.creatures[0].hp < scene.opponent.creatures[0].max_hp, \
           "No battle occurred during the test"

    # If we've reached this point without any unexpected exceptions, the test passes
    assert True

def test_player_wins_due_to_speed_advantage(app):
    player = app.create_player("test_player")
    player.display_name = "Player"
    player.creatures[0].speed = 5  # Set player's creature speed higher than opponent's
    player.creatures[0].attack = 6  # Increase player's attack to ensure victory

    scene = MainGameScene(app, player)
    runner = ThreadedSceneRunner()
    runner.start_game(scene)

    # Player's first turn
    choices = runner.dequeue_wait_for_choice(player)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)

    # Opponent's first turn
    choices = runner.dequeue_wait_for_choice(scene.opponent)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)

    # Player's second turn
    choices = runner.dequeue_wait_for_choice(player)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)

    # Opponent's second turn
    choices = runner.dequeue_wait_for_choice(scene.opponent)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)

    assert runner.dequeue_transition_to_scene() == "MainMenuScene"
    assert scene.player_creature.hp > 0
    assert scene.opponent_creature.hp == 0

def test_opponent_wins_with_equal_speed(app):
    player = app.create_player("test_player")
    player.display_name = "Player"
    player.creatures[0].speed = 3  # Set player's creature speed equal to opponent's
    player.creatures[0].defense = 1  # Decrease player's defense to ensure opponent victory

    scene = MainGameScene(app, player)
    runner = ThreadedSceneRunner()
    runner.start_game(scene)

    # Player's first turn
    choices = runner.dequeue_wait_for_choice(player)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)

    # Opponent's first turn
    choices = runner.dequeue_wait_for_choice(scene.opponent)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)

    # Player's second turn
    choices = runner.dequeue_wait_for_choice(player)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)

    # Opponent's second turn
    choices = runner.dequeue_wait_for_choice(scene.opponent)
    tackle = find_button(choices, "Tackle")
    runner.make_choice(tackle)

    assert runner.dequeue_transition_to_scene() == "MainMenuScene"
    assert scene.player_creature.hp == 0
    assert scene.opponent_creature.hp > 0
