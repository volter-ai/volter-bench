import pytest
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_button, find_select_thing
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.lib import HumanListener
from unittest.mock import patch
from mini_game_engine.engine.lib import RandomModeGracefulExit


class TestMainGameSceneRandomRun:
    @pytest.fixture
    def app(self):
        return App()

    def test_main_game_scene_random_run(self, app):
        for i in range(10):
            print(f"starting random run iteration {i}")
            HumanListener.random_mode = True
            HumanListener.random_mode_counter = 30  # More moves needed for the complex MainGameScene

            player = app.create_player(f"player_{i}")
            main_game_scene = MainGameScene(app, player)

            class TransitionFromScene(Exception):
                pass

            def exit_scene(*args, **kwargs):
                raise TransitionFromScene()

            with patch.object(MainGameScene, '_transition_to_scene', side_effect=exit_scene) as mock_transition, \
                    patch.object(MainGameScene, '_quit_whole_game') as mock_quit:

                try:
                    main_game_scene.run()
                except TransitionFromScene:
                    print(f"exiting target scene `MainGameScene` so ending run {i}")
                except RandomModeGracefulExit:
                    print(f"`random_mode_counter` reached 0 and the game did not crash. Ending run {i} gracefully")
                else:
                    assert mock_transition.called or mock_quit.called, "scene was not exited in an expected manner"

                    if mock_quit.called:
                        print("_quit_whole_game called")
                    if mock_transition.called:
                        print("_transition_to_scene called")
                finally:
                    mock_transition.reset_mock()
                    mock_quit.reset_mock()

class TestMainGameScene:
    @pytest.fixture
    def app(self):
        return App()

    @pytest.fixture
    def player(self, app):
        return app.create_player("test_player")

    @pytest.fixture
    def main_game_scene(self, app, player):
        return MainGameScene(app, player)

    def test_main_game_scene_full_battle(self, app, player, main_game_scene):
        runner = ThreadedSceneRunner()
        runner.start_game(main_game_scene)

        # Initial state check
        assert player.active_creature.prototype_id == "bubwool"
        assert main_game_scene.bot.active_creature.prototype_id == "scizard"

        while True:
            # Player's turn
            choices = runner.dequeue_wait_for_choice(player)
            attack_button = find_button(choices, "Attack")
            runner.make_choice(attack_button)

            choices = runner.dequeue_wait_for_choice(player)
            skill = find_select_thing(choices, choices[0].thing.prototype_id)  # Choose the first available skill
            runner.make_choice(skill)

            # Bot's turn
            choices = runner.dequeue_wait_for_choice(main_game_scene.bot)
            attack_button = find_button(choices, "Attack")
            runner.make_choice(attack_button)

            choices = runner.dequeue_wait_for_choice(main_game_scene.bot)
            skill = find_select_thing(choices, choices[0].thing.prototype_id)  # Choose the first available skill
            runner.make_choice(skill)

            # Check if the battle has ended
            try:
                scene_name = runner.dequeue_transition_to_scene()
                assert scene_name == "MainMenuScene"
                break
            except ValueError:
                # Battle hasn't ended, continue to next turn
                pass

            # If a creature has fainted, we need to swap
            if player.active_creature.hp == 0:
                choices = runner.dequeue_wait_for_choice(player)
                new_creature = find_select_thing(choices, choices[0].thing.prototype_id)  # Choose the first available creature
                runner.make_choice(new_creature)

            if main_game_scene.bot.active_creature.hp == 0:
                choices = runner.dequeue_wait_for_choice(main_game_scene.bot)
                new_creature = find_select_thing(choices, choices[0].thing.prototype_id)  # Choose the first available creature
                runner.make_choice(new_creature)

        # Final state check
        assert all(creature.hp == 0 for creature in player.creatures) or all(creature.hp == 0 for creature in main_game_scene.bot.creatures)
