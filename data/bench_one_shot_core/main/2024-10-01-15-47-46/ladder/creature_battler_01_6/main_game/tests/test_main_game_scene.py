import pytest
from mini_game_engine.engine.lib import AbstractApp, RandomModeGracefulExit, HumanListener
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_select_thing
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene


@pytest.fixture
def app():
    return App()

def test_main_game_scene(app):
    HumanListener.random_mode = True
    player = app.create_player("test_player")
    
    run_count = 0
    for _ in range(10):
        try:
            run_count += 1  # Increment run_count before transition_to_scene
            app.transition_to_scene("MainGameScene", player=player)
        except RandomModeGracefulExit:
            # Consider this a successful run and break the loop
            break
        except AbstractApp._QuitWholeGame:
            break

    assert run_count > 0, "The game should run at least once before quitting"

class TestMainGameScene:
    @pytest.fixture
    def player(self, app):
        player = app.create_player("test_player")
        player.display_name = "Player 1"
        return player

    def test_player_wins(self, app, player):
        scene = MainGameScene(app, player)
        scene.opponent_creature.hp = 3

        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        # Player turn
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        # Opponent turn
        choices = runner.dequeue_wait_for_choice(scene.opponent)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        # Check final state
        assert scene.player_creature.hp == 7
        assert scene.opponent_creature.hp == 0

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"

    def test_opponent_wins(self, app, player):
        scene = MainGameScene(app, player)
        scene.player_creature.hp = 3

        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        # Player turn
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        # Opponent turn
        choices = runner.dequeue_wait_for_choice(scene.opponent)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        # Check final state
        assert scene.player_creature.hp == 0
        assert scene.opponent_creature.hp == 7

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"

    def test_multiple_turns(self, app, player):
        scene = MainGameScene(app, player)

        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        # Turn 1
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(scene.opponent)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        assert scene.player_creature.hp == 7
        assert scene.opponent_creature.hp == 7

        # Turn 2
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(scene.opponent)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        assert scene.player_creature.hp == 4
        assert scene.opponent_creature.hp == 4

        # Turn 3
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(scene.opponent)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        assert scene.player_creature.hp == 1
        assert scene.opponent_creature.hp == 1

        # Turn 4 (final turn)
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(scene.opponent)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        assert scene.player_creature.hp == 0
        assert scene.opponent_creature.hp == 0

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"

    def test_reset_creatures(self, app, player):
        scene = MainGameScene(app, player)
        scene.player_creature.hp = 5
        scene.opponent_creature.hp = 5

        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        # One turn to end the battle
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(scene.opponent)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        # Check that creatures are reset before transitioning
        assert runner.dequeue_transition_to_scene() == "MainMenuScene"
        assert scene.player_creature.hp == scene.player_creature.max_hp == 10
        assert scene.opponent_creature.hp == scene.opponent_creature.max_hp == 10
