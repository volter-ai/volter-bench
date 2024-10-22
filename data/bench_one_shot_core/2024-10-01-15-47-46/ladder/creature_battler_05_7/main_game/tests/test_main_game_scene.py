import pytest
from main_game.main import App
from main_game.models import Creature
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.lib import (AbstractApp, HumanListener,
                                         RandomModeGracefulExit)
from mini_game_engine.engine.qa_utils import (ThreadedSceneRunner, find_button,
                                              find_select_thing)


@pytest.fixture
def app():
    return App()

def test_main_game_scene(app):
    HumanListener.random_mode = True
    player = app.create_player("test_player")
    
    for _ in range(10):
        HumanListener.random_mode_counter = 100  # Reset the counter before each run
        try:
            app.transition_to_scene("MainGameScene", player=player)
        except (RandomModeGracefulExit, AbstractApp._QuitWholeGame):
            # These exceptions are expected when the random mode counter reaches zero
            # or when the game ends gracefully
            pass

def test_main_game_scene_full_battle(app):
    # Setup
    player1 = app.create_player("test_player1")
    player1.display_name = "Player 1"

    # Ensure the player has the correct creatures with specific speeds
    bubwool = Creature.from_prototype_id("bubwool")
    bubwool.speed = 20
    dumbird1 = Creature.from_prototype_id("dumbird")
    dumbird1.speed = 10
    player1.creatures = [bubwool, dumbird1]

    scene = MainGameScene(app, player1)

    runner = ThreadedSceneRunner()
    runner.start_game(scene)

    # Player 1 turn
    choices = runner.dequeue_wait_for_choice(player1)
    attack_choice = find_button(choices, "Attack")
    runner.make_choice(attack_choice)

    choices = runner.dequeue_wait_for_choice(player1)
    tackle_choice = find_select_thing(choices, "tackle")
    runner.make_choice(tackle_choice)

    # Handle random tiebreaker
    random_call = runner.dequeue_random_call()
    assert random_call['function'] == 'random'

    # Check state after first round
    assert scene.player.active_creature.hp < scene.player.active_creature.max_hp
    assert scene.opponent.active_creature.hp < scene.opponent.active_creature.max_hp

    # Player 1 turn (swap)
    choices = runner.dequeue_wait_for_choice(player1)
    swap_choice = find_button(choices, "Swap")
    runner.make_choice(swap_choice)

    choices = runner.dequeue_wait_for_choice(player1)
    dumbird_choice = find_select_thing(choices, "dumbird")
    runner.make_choice(dumbird_choice)

    # Handle random tiebreaker
    random_call = runner.dequeue_random_call()
    assert random_call['function'] == 'random'

    # Check state after second round
    assert scene.player.active_creature.prototype_id == "dumbird"
    assert scene.player.active_creature.hp < scene.player.active_creature.max_hp

    # Player 1 turn
    choices = runner.dequeue_wait_for_choice(player1)
    attack_choice = find_button(choices, "Attack")
    runner.make_choice(attack_choice)

    choices = runner.dequeue_wait_for_choice(player1)
    tackle_choice = find_select_thing(choices, "tackle")
    runner.make_choice(tackle_choice)

    # Handle random tiebreaker
    random_call = runner.dequeue_random_call()
    assert random_call['function'] == 'random'

    # Player 1's Dumbird might faint, forced to swap
    if scene.player.active_creature.hp == 0:
        choices = runner.dequeue_wait_for_choice(player1)
        bubwool_choice = find_select_thing(choices, "bubwool")
        runner.make_choice(bubwool_choice)

    # Player 1 turn
    choices = runner.dequeue_wait_for_choice(player1)
    attack_choice = find_button(choices, "Attack")
    runner.make_choice(attack_choice)

    choices = runner.dequeue_wait_for_choice(player1)
    skill_choice = find_select_thing(choices, scene.player.active_creature.skills[0].prototype_id)
    runner.make_choice(skill_choice)

    # Handle random tiebreaker
    random_call = runner.dequeue_random_call()
    assert random_call['function'] == 'random'

    # Continue the battle until it ends
    while True:
        try:
            choices = runner.dequeue_wait_for_choice(player1)
            attack_choice = find_button(choices, "Attack")
            runner.make_choice(attack_choice)

            choices = runner.dequeue_wait_for_choice(player1)
            skill_choice = find_select_thing(choices, scene.player.active_creature.skills[0].prototype_id)
            runner.make_choice(skill_choice)

            # Handle random tiebreaker
            random_call = runner.dequeue_random_call()
            assert random_call['function'] == 'random'

            # Check if player needs to swap
            if scene.player.active_creature.hp == 0:
                available_creatures = [c for c in scene.player.creatures if c.hp > 0]
                if available_creatures:
                    choices = runner.dequeue_wait_for_choice(player1)
                    swap_choice = find_select_thing(choices, available_creatures[0].prototype_id)
                    runner.make_choice(swap_choice)
                else:
                    break  # Player has lost
        except TimeoutError:
            break  # Battle has ended

    # Battle should end here
    assert runner.dequeue_transition_to_scene() == "MainMenuScene"

    # Check final state
    assert (all(creature.hp == 0 for creature in scene.player.creatures) or 
            all(creature.hp == 0 for creature in scene.opponent.creatures))
