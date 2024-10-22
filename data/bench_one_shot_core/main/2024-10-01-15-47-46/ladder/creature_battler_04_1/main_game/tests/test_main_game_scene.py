import pytest
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_button
from mini_game_engine.engine.lib import AbstractApp, RandomModeGracefulExit, HumanListener


@pytest.fixture
def app():
    return App()

def test_main_game_scene(app):
    HumanListener.random_mode = True
    player = app.create_player("test_player")
    
    for _ in range(10):
        try:
            app.transition_to_scene("MainGameScene", player=player)
        except RandomModeGracefulExit:
            break
        except AbstractApp._QuitWholeGame:
            # This exception indicates a successful game completion
            break

    HumanListener.random_mode = False

class TestMainGameScene:
    def test_player_loses_type_disadvantage(self, app):
        player = app.create_player("test_player")
        player.display_name = "Player"
        opponent = app.create_bot("basic_opponent")
        opponent.display_name = "Opponent"

        scene = MainGameScene(app, player)
        scene.opponent = opponent

        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        # Round 1
        choices = runner.dequeue_wait_for_choice(player)
        lick_skill = find_button(choices, "Lick")
        runner.make_choice(lick_skill)

        choices = runner.dequeue_wait_for_choice(opponent)
        tackle_skill = find_button(choices, "Tackle")
        runner.make_choice(tackle_skill)

        # Round 2
        choices = runner.dequeue_wait_for_choice(player)
        assert scene.opponent_creature.hp == 34
        assert scene.player_creature.hp == 24
        lick_skill = find_button(choices, "Lick")
        runner.make_choice(lick_skill)

        choices = runner.dequeue_wait_for_choice(opponent)
        tackle_skill = find_button(choices, "Tackle")
        runner.make_choice(tackle_skill)

        # Round 3
        choices = runner.dequeue_wait_for_choice(player)
        assert scene.opponent_creature.hp == 28
        assert scene.player_creature.hp == 16
        lick_skill = find_button(choices, "Lick")
        runner.make_choice(lick_skill)

        choices = runner.dequeue_wait_for_choice(opponent)
        tackle_skill = find_button(choices, "Tackle")
        runner.make_choice(tackle_skill)

        # Round 4 - Check HP before final round
        choices = runner.dequeue_wait_for_choice(player)
        assert scene.opponent_creature.hp == 22
        assert scene.player_creature.hp == 8
        lick_skill = find_button(choices, "Lick")
        runner.make_choice(lick_skill)

        choices = runner.dequeue_wait_for_choice(opponent)
        tackle_skill = find_button(choices, "Tackle")
        runner.make_choice(tackle_skill)

        # Battle should end after this round
        assert runner.dequeue_transition_to_scene() == "MainMenuScene"

    def test_skill_execution_order_with_equal_speed(self, app):
        player = app.create_player("test_player")
        player.display_name = "Player"
        opponent = app.create_bot("basic_opponent")
        opponent.display_name = "Opponent"

        scene = MainGameScene(app, player)
        scene.opponent = opponent

        # Modify Bubwool's speed to be equal to Scizard's
        scene.player_creature.speed = scene.opponent_creature.speed

        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        initial_player_hp = scene.player_creature.hp
        initial_opponent_hp = scene.opponent_creature.hp

        # Round 1
        choices = runner.dequeue_wait_for_choice(player)
        tackle_skill = find_button(choices, "Tackle")
        runner.make_choice(tackle_skill)

        choices = runner.dequeue_wait_for_choice(opponent)
        fireball_skill = find_button(choices, "Fireball")
        runner.make_choice(fireball_skill)

        # Check that both skills were executed
        assert scene.player_creature.hp < initial_player_hp
        assert scene.opponent_creature.hp < initial_opponent_hp

        # Round 2
        choices = runner.dequeue_wait_for_choice(player)
        tackle_skill = find_button(choices, "Tackle")
        runner.make_choice(tackle_skill)

        choices = runner.dequeue_wait_for_choice(opponent)
        fireball_skill = find_button(choices, "Fireball")
        runner.make_choice(fireball_skill)

        # Round 3
        choices = runner.dequeue_wait_for_choice(player)
        tackle_skill = find_button(choices, "Tackle")
        runner.make_choice(tackle_skill)

        choices = runner.dequeue_wait_for_choice(opponent)
        fireball_skill = find_button(choices, "Fireball")
        runner.make_choice(fireball_skill)

        # Round 4
        choices = runner.dequeue_wait_for_choice(player)
        tackle_skill = find_button(choices, "Tackle")
        runner.make_choice(tackle_skill)

        choices = runner.dequeue_wait_for_choice(opponent)
        fireball_skill = find_button(choices, "Fireball")
        runner.make_choice(fireball_skill)

        # Round 5 (final round)
        choices = runner.dequeue_wait_for_choice(player)
        tackle_skill = find_button(choices, "Tackle")
        runner.make_choice(tackle_skill)

        choices = runner.dequeue_wait_for_choice(opponent)
        fireball_skill = find_button(choices, "Fireball")
        runner.make_choice(fireball_skill)

        # Battle should end after this round
        assert runner.dequeue_transition_to_scene() == "MainMenuScene"

        # Final check - one creature should be defeated
        assert scene.player_creature.hp <= 0 or scene.opponent_creature.hp <= 0
