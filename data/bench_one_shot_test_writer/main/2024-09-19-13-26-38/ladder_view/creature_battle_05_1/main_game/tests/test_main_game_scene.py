import pytest
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_button, find_select_thing
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.lib import HumanListener
from unittest.mock import patch
from mini_game_engine.engine.lib import RandomModeGracefulExit
from mini_game_engine.engine.lib import Button


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

    def test_normal_battle_flow(self, app, player, main_game_scene):
        runner = ThreadedSceneRunner()
        runner.start_game(main_game_scene)

        battle_ended = False
        while not battle_ended:
            # Player's turn
            self.handle_turn(runner, player)

            # Bot's turn
            self.handle_turn(runner, main_game_scene.bot)

            # Check if battle has ended
            if all(c.hp <= 0 for c in player.creatures) or all(c.hp <= 0 for c in main_game_scene.bot.creatures):
                battle_ended = True

        # Verify that the battle ends and transitions to the MainMenuScene
        assert runner.dequeue_transition_to_scene() == "MainMenuScene"

    def test_forced_swap(self, app, player, main_game_scene):
        runner = ThreadedSceneRunner()
        runner.start_game(main_game_scene)

        # Play the battle until the player's active creature faints
        while player.active_creature.hp > 0:
            self.handle_turn(runner, player)
            self.handle_turn(runner, main_game_scene.bot)

        # Handle the forced swap and the following player's turn
        self.handle_turn(runner, player)

        # Verify that the battle continues with the new active creature
        assert player.active_creature.hp > 0
        assert player.active_creature != player.creatures[0]  # Should not be the original creature

        # Bot's turn
        self.handle_turn(runner, main_game_scene.bot)

        # Verify that the battle continues (no transition to MainMenuScene)
        with pytest.raises(TimeoutError):
            runner.dequeue_transition_to_scene()

    def handle_turn(self, runner, player):
        choices = runner.dequeue_wait_for_choice(player)
        if any(isinstance(choice, Button) for choice in choices):
            attack_button = find_button(choices, "Attack")
            runner.make_choice(attack_button)

            choices = runner.dequeue_wait_for_choice(player)
            skill_choice = find_select_thing(choices, player.active_creature.skills[0].prototype_id)
            runner.make_choice(skill_choice)
        else:
            # Forced swap
            swap_choice = find_select_thing(choices, [c for c in player.creatures if c.hp > 0][0].prototype_id)
            runner.make_choice(swap_choice)
            
            # Continue with the player's turn after forced swap
            choices = runner.dequeue_wait_for_choice(player)
            attack_button = find_button(choices, "Attack")
            runner.make_choice(attack_button)

            choices = runner.dequeue_wait_for_choice(player)
            skill_choice = find_select_thing(choices, player.active_creature.skills[0].prototype_id)
            runner.make_choice(skill_choice)
