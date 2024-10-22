import pytest
from main_game.models import Player
from main_game.scenes.main_game_scene import MainGameScene
from main_game.scenes.main_menu_scene import MainMenuScene
from mini_game_engine.engine.lib import (AbstractApp, BotListener,
                                         HumanListener, RandomModeGracefulExit)
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
    HumanListener.random_mode_counter = 1000  # Increase the counter to allow for more interactions

    scene = MainGameScene(app, player)
    
    try:
        scene.run()
    except (AbstractApp._QuitWholeGame, RandomModeGracefulExit):
        # These exceptions are expected when the game ends or random mode finishes
        pass
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")

    # If we reach this point without any unexpected exceptions, the test is considered successful
    assert True

def test_battle_outcome(app, player):
    scene = MainGameScene(app, player)
    scene.player.display_name = "Player"
    scene.opponent.display_name = "Opponent"

    runner = ThreadedSceneRunner()
    runner.start_game(scene)

    # First round
    player_choices = runner.dequeue_wait_for_choice(scene.player)
    player_choice = find_button(player_choices, "Tackle")
    runner.make_choice(player_choice)

    opponent_choices = runner.dequeue_wait_for_choice(scene.opponent)
    opponent_choice = find_button(opponent_choices, "Tackle")
    runner.make_choice(opponent_choice)

    assert scene.player_creature.hp == 6
    assert scene.opponent_creature.hp == 8

    # Second round
    player_choices = runner.dequeue_wait_for_choice(scene.player)
    player_choice = find_button(player_choices, "Tackle")
    runner.make_choice(player_choice)

    opponent_choices = runner.dequeue_wait_for_choice(scene.opponent)
    opponent_choice = find_button(opponent_choices, "Tackle")
    runner.make_choice(opponent_choice)

    assert scene.player_creature.hp == 2
    assert scene.opponent_creature.hp == 5

    # Third round
    player_choices = runner.dequeue_wait_for_choice(scene.player)
    player_choice = find_button(player_choices, "Tackle")
    runner.make_choice(player_choice)

    opponent_choices = runner.dequeue_wait_for_choice(scene.opponent)
    opponent_choice = find_button(opponent_choices, "Tackle")
    runner.make_choice(opponent_choice)

    assert scene.player_creature.hp == 0
    assert scene.opponent_creature.hp == 2

    assert runner.dequeue_transition_to_scene() == "MainMenuScene"

def test_player_loses_battle(app, player):
    scene = MainGameScene(app, player)
    scene.player.display_name = "Player"
    scene.opponent.display_name = "Opponent"
    
    # Modify player's creature to have very low HP
    scene.player_creature.hp = 1
    scene.player_creature.max_hp = 1

    runner = ThreadedSceneRunner()
    runner.start_game(scene)

    player_choices = runner.dequeue_wait_for_choice(scene.player)
    player_choice = find_button(player_choices, "Tackle")
    runner.make_choice(player_choice)

    opponent_choices = runner.dequeue_wait_for_choice(scene.opponent)
    opponent_choice = find_button(opponent_choices, "Tackle")
    runner.make_choice(opponent_choice)

    assert scene.player_creature.hp == 0
    assert runner.dequeue_transition_to_scene() == "MainMenuScene"

def test_equal_speed_scenario(app, player):
    scene = MainGameScene(app, player)
    scene.player.display_name = "Player"
    scene.opponent.display_name = "Opponent"
    
    # Modify player's creature speed to be equal to opponent's
    scene.player_creature.speed = 3

    runner = ThreadedSceneRunner()
    runner.start_game(scene)

    # Battle continues until one creature's HP reaches 0
    while scene.player_creature.hp > 0 and scene.opponent_creature.hp > 0:
        player_choices = runner.dequeue_wait_for_choice(scene.player)
        player_choice = find_button(player_choices, "Tackle")
        runner.make_choice(player_choice)

        opponent_choices = runner.dequeue_wait_for_choice(scene.opponent)
        opponent_choice = find_button(opponent_choices, "Tackle")
        runner.make_choice(opponent_choice)

    # Assert that one of the creatures has 0 HP
    assert scene.player_creature.hp == 0 or scene.opponent_creature.hp == 0

    # Assert that the other creature has more than 0 HP
    assert scene.player_creature.hp > 0 or scene.opponent_creature.hp > 0

    assert runner.dequeue_transition_to_scene() == "MainMenuScene"
