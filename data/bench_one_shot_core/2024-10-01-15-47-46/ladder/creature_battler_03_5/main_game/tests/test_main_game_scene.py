import pytest
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.lib import (AbstractApp, HumanListener,
                                         RandomModeGracefulExit)
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_button


@pytest.fixture
def app():
    return App()

def test_main_game_scene(app):
    HumanListener.random_mode = True
    player = app.create_player("test_player")
    
    scene = MainGameScene(app, player)
    
    try:
        scene.run()
    except AbstractApp._QuitWholeGame:
        # This exception indicates that the game has ended normally
        pass
    except RandomModeGracefulExit:
        # This exception is also acceptable as it indicates the random mode has completed
        pass
    
    # Assert that the battle count has reached the maximum
    assert scene.battle_count == scene.max_battles, f"Expected {scene.max_battles} battles, but only {scene.battle_count} were played"

    HumanListener.random_mode = False

def test_player_wins_all_battles(app):
    player = app.create_player("test_player")
    player.display_name = "Player 1"
    opponent = app.create_bot("basic_opponent")
    opponent.display_name = "Player 2"

    # Modify player's creature (Bubwool)
    player.creatures[0].speed = 10
    player.creatures[0].attack = 10
    player.creatures[0].defense = 5

    # Modify opponent's creature (Scizard)
    opponent.creatures[0].speed = 5
    opponent.creatures[0].defense = 1
    opponent.creatures[0].hp = 15
    opponent.creatures[0].max_hp = 15

    scene = MainGameScene(app, player)
    scene.opponent = opponent

    runner = ThreadedSceneRunner()
    runner.start_game(scene)

    for battle in range(3):
        # Player's turn
        choices = runner.dequeue_wait_for_choice(player)
        lick_skill = find_button(choices, "Lick")
        runner.make_choice(lick_skill)

        # Opponent's turn
        choices = runner.dequeue_wait_for_choice(opponent)
        tackle_skill = find_button(choices, "Tackle")
        runner.make_choice(tackle_skill)

        # Battle end
        if battle < 2:
            choices = runner.dequeue_wait_for_choice(player)
            continue_button = find_button(choices, "Continue")
            runner.make_choice(continue_button)

    assert runner.dequeue_transition_to_scene() == "MainMenuScene"
    assert scene.battle_count == 3
    assert scene.player_creature.hp > 0
    assert scene.opponent_creature.hp <= 0

def test_player_loses_and_quits(app):
    player = app.create_player("test_player")
    player.display_name = "Player 1"
    opponent = app.create_bot("basic_opponent")
    opponent.display_name = "Player 2"

    # Modify player's creature (Bubwool)
    player.creatures[0].speed = 5
    player.creatures[0].defense = 0
    player.creatures[0].hp = 1
    player.creatures[0].max_hp = 1

    # Modify opponent's creature (Scizard)
    opponent.creatures[0].speed = 10
    opponent.creatures[0].attack = 30

    scene = MainGameScene(app, player)
    scene.opponent = opponent

    runner = ThreadedSceneRunner()
    runner.start_game(scene)

    # Player's turn
    choices = runner.dequeue_wait_for_choice(player)
    tackle_skill = find_button(choices, "Tackle")
    runner.make_choice(tackle_skill)

    # Opponent's turn
    choices = runner.dequeue_wait_for_choice(opponent)
    fireball_skill = find_button(choices, "Fireball")
    runner.make_choice(fireball_skill)

    # Battle end
    choices = runner.dequeue_wait_for_choice(player)
    quit_button = find_button(choices, "Quit to Main Menu")
    runner.make_choice(quit_button)

    assert runner.dequeue_transition_to_scene() == "MainMenuScene"
    assert scene.battle_count == 1
    assert scene.player_creature.hp < scene.opponent_creature.hp
    assert scene.opponent_creature.hp > 0
