import pytest
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_button
from mini_game_engine.engine.lib import RandomModeGracefulExit, HumanListener, AbstractApp


@pytest.fixture
def app():
    return App()

def test_main_game_scene(app):
    HumanListener.random_mode = True
    HumanListener.random_mode_counter = 100
    player = app.create_player("test_player")

    iterations = 0

    def count_iterations(scene_name, **kwargs):
        nonlocal iterations
        iterations += 1
        if scene_name == "MainGameScene":
            raise RandomModeGracefulExit()

    app.transition_to_scene = count_iterations

    try:
        app.run(player)
    except (RandomModeGracefulExit, AbstractApp._QuitWholeGame):
        pass

    assert iterations > 0, "The game should run at least once"

class TestMainGameScene:
    def test_player_wins_battle(self, app):
        player = app.create_player("test_player")
        player.display_name = "Player 1"
        bot = app.create_bot("default_player")
        bot.display_name = "Player 2"

        scene = MainGameScene(app, player)
        scene.opponent = bot
        scene.player_creature.hp = 10
        scene.opponent_creature.hp = 3

        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        # Turn 1: Player chooses Tackle
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        # Turn 1: Bot chooses Tackle
        choices = runner.dequeue_wait_for_choice(bot)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        # Check final state
        assert scene.player_creature.hp == 7
        assert scene.opponent_creature.hp == 0

        # Check scene transition
        assert runner.dequeue_transition_to_scene() == "MainMenuScene"

    def test_bot_wins_battle(self, app):
        player = app.create_player("test_player")
        player.display_name = "Player 1"
        bot = app.create_bot("default_player")
        bot.display_name = "Player 2"

        scene = MainGameScene(app, player)
        scene.opponent = bot
        scene.player_creature.hp = 3
        scene.opponent_creature.hp = 10

        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        # Turn 1: Player chooses Tackle
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        # Turn 1: Bot chooses Tackle
        choices = runner.dequeue_wait_for_choice(bot)
        tackle = find_button(choices, "Tackle")
        runner.make_choice(tackle)

        # Check final state
        assert scene.player_creature.hp == 0
        assert scene.opponent_creature.hp == 7

        # Check scene transition
        assert runner.dequeue_transition_to_scene() == "MainMenuScene"
