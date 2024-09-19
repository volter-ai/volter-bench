import pytest
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_select_thing
from unittest.mock import patch
import math


class TestMainGameSceneRandomRun:
    @pytest.fixture
    def app(self):
        return App()

    def test_main_game_scene_random_run(self, app):
        for i in range(10):
            print(f"starting random run iteration {i}")
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 30  # Increased to 30 for more complex scene

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            class TransitionFromScene(Exception):
                pass

            def exit_scene(*args, **kwargs):
                raise TransitionFromScene()

            with patch.object(MainGameScene, '_transition_to_scene', side_effect=exit_scene) as mock_transition:
                try:
                    main_game_scene.run()
                except TransitionFromScene:
                    print(f"exiting target scene `MainGameScene` so ending run {i}")
                except RandomModeGracefulExit:
                    print(f"`random_mode_counter` reached 0 and the game did not crash. Ending run {i} gracefully")
                else:
                    assert mock_transition.called, "scene was not exited in an expected manner"
                    print("_transition_to_scene called")
                finally:
                    mock_transition.reset_mock()

class TestMainGameScene:
    @pytest.fixture
    def app(self):
        return App()

    @pytest.fixture
    def player(self, app):
        return app.create_player("test_player")

    @pytest.fixture
    def scene(self, app, player):
        return MainGameScene(app, player)

    def test_player_wins(self, app, player, scene):
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        initial_player_hp = scene.player_creature.hp
        initial_foe_hp = scene.foe_creature.hp
        tackle_damage = scene.player_creature.skills[0].damage

        rounds_to_win = math.ceil(initial_foe_hp / tackle_damage)

        for _ in range(rounds_to_win):
            choices = runner.dequeue_wait_for_choice(player)
            tackle = find_select_thing(choices, "tackle")
            runner.make_choice(tackle)

            choices = runner.dequeue_wait_for_choice(scene.foe)
            tackle = find_select_thing(choices, "tackle")
            runner.make_choice(tackle)

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"
        assert scene.player_creature.hp > 0
        assert scene.foe_creature.hp <= 0

    def test_player_loses(self, app, player, scene):
        runner = ThreadedSceneRunner()
        scene.player_creature.hp = 3  # Set player's creature HP low
        runner.start_game(scene)

        # Player's turn
        choices = runner.dequeue_wait_for_choice(player)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        # Foe's turn
        choices = runner.dequeue_wait_for_choice(scene.foe)
        tackle = find_select_thing(choices, "tackle")
        runner.make_choice(tackle)

        assert runner.dequeue_transition_to_scene() == "MainMenuScene"
        assert scene.player_creature.hp <= 0
        assert scene.foe_creature.hp > 0

    def test_multiple_turns(self, app, player, scene):
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        initial_player_hp = scene.player_creature.hp
        initial_foe_hp = scene.foe_creature.hp
        tackle_damage = scene.player_creature.skills[0].damage

        max_rounds = 5
        battle_ended = False

        for i in range(max_rounds):
            # Player's turn
            choices = runner.dequeue_wait_for_choice(player)
            tackle = find_select_thing(choices, "tackle")
            runner.make_choice(tackle)

            # Foe's turn
            choices = runner.dequeue_wait_for_choice(scene.foe)
            tackle = find_select_thing(choices, "tackle")
            runner.make_choice(tackle)

            # Check if battle ended after both turns
            try:
                assert runner.dequeue_transition_to_scene() == "MainMenuScene"
                battle_ended = True
                break
            except TimeoutError:
                pass

            # Assert HP values after each full round
            assert scene.player_creature.hp == initial_player_hp - (i + 1) * tackle_damage
            assert scene.foe_creature.hp == initial_foe_hp - (i + 1) * tackle_damage

        assert battle_ended, "Battle did not end within the expected number of turns"
        
        # Final assertions
        if scene.player_creature.hp <= 0:
            assert scene.foe_creature.hp > 0
        else:
            assert scene.foe_creature.hp <= 0
            assert scene.player_creature.hp > 0
