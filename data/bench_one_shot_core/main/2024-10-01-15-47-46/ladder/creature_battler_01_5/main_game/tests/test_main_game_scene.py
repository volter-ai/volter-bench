import pytest
from main_game.main import App
from mini_game_engine.engine.lib import HumanListener, AbstractApp
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_select_thing
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.lib import RandomModeGracefulExit


@pytest.fixture
def app():
    return App()

def test_main_game_scene(app):
    HumanListener.random_mode = True
    player = app.create_player("test_player")
    
    max_attempts = 20
    game_ran = False

    for _ in range(max_attempts):
        try:
            app.transition_to_scene("MainGameScene", player=player)
            game_ran = True
            break
        except RandomModeGracefulExit:
            # Consider this a successful run
            game_ran = True
            break
        except AbstractApp._QuitWholeGame:
            # Game completed successfully
            game_ran = True
            break
    
    assert game_ran, f"Game did not run successfully in {max_attempts} attempts"

def test_player_wins_battle(app):
    player = app.create_player("test_player")
    player.display_name = "Player 1"
    scene = MainGameScene(app, player)
    opponent = scene.opponent
    opponent.display_name = "Player 2"

    runner = ThreadedSceneRunner()
    runner.start_game(scene)

    for _ in range(4):
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(opponent)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        assert scene.player_creature.hp == max(0, 10 - (3 * (_ + 1)))
        assert scene.opponent_creature.hp == max(0, 10 - (3 * (_ + 1)))

    choices = runner.dequeue_wait_for_choice(player)
    tackle = find_select_thing(choices, "tackle")
    runner.make_choice(tackle)

    assert scene.player_creature.hp == 1
    assert scene.opponent_creature.hp == 0

    assert runner.dequeue_transition_to_scene() == "MainMenuScene"

def test_player_loses_battle(app):
    player = app.create_player("test_player")
    player.display_name = "Player 1"
    scene = MainGameScene(app, player)
    opponent = scene.opponent
    opponent.display_name = "Player 2"
    scene.player_creature.hp = 3  # Set player's creature HP to 3 to ensure they lose in one hit

    runner = ThreadedSceneRunner()
    runner.start_game(scene)

    choices = runner.dequeue_wait_for_choice(player)
    tackle = find_select_thing(choices, "tackle")
    runner.make_choice(tackle)

    choices = runner.dequeue_wait_for_choice(opponent)
    tackle = find_select_thing(choices, "tackle")
    runner.make_choice(tackle)

    assert scene.player_creature.hp == 0
    assert scene.opponent_creature.hp == 7

    assert runner.dequeue_transition_to_scene() == "MainMenuScene"
