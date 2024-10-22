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
    
    completed_games = 0
    max_attempts = 10

    for _ in range(max_attempts):
        try:
            app.transition_to_scene("MainGameScene", player=player)
        except AbstractApp._QuitWholeGame:
            # This exception indicates a successful game completion
            completed_games += 1
        except RandomModeGracefulExit:
            # This exception is expected and should be ignored
            pass

        if completed_games > 0:
            break  # We've successfully completed at least one game

    HumanListener.random_mode = False

    assert completed_games > 0, f"Failed to complete any games in {max_attempts} attempts"

class TestMainGameScene:
    @pytest.fixture
    def player(self, app):
        return app.create_player("test_player")

    @pytest.fixture
    def opponent(self, app):
        return app.create_bot("basic_opponent")

    def test_player_wins_type_advantage(self, app, player, opponent):
        scene = MainGameScene(app, player)
        scene.opponent = opponent
        scene.player_creature.attack = 20  # Increase player's attack to ensure victory
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        choices = runner.dequeue_wait_for_choice(player)
        lick = find_button(choices, "Lick")
        runner.make_choice(lick)

        choices = runner.dequeue_wait_for_choice(opponent)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(player)
        lick = find_button(choices, "Lick")
        runner.make_choice(lick)

        choices = runner.dequeue_wait_for_choice(opponent)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"

        assert scene.player_creature.hp > 0
        assert scene.opponent_creature.hp <= 0

    def test_opponent_wins_higher_stats(self, app, player, opponent):
        scene = MainGameScene(app, player)
        scene.opponent = opponent
        scene.opponent_creature.attack = 20  # Increase opponent's attack to ensure victory
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(opponent)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(opponent)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"

        assert scene.player_creature.hp <= 0
        assert scene.opponent_creature.hp > 0

    def test_equal_speed_scenario(self, app, player, opponent):
        scene = MainGameScene(app, player)
        scene.opponent = opponent
        scene.player_creature.speed = 11  # Set to match opponent's speed
        scene.player_creature.hp = 15  # Reduce HP to end battle faster
        scene.opponent_creature.hp = 15  # Reduce HP to end battle faster
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(opponent)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        choices = runner.dequeue_wait_for_choice(opponent)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"

        assert (scene.player_creature.hp <= 0 or scene.opponent_creature.hp <= 0)
        assert (scene.player_creature.hp > 0 or scene.opponent_creature.hp > 0)
