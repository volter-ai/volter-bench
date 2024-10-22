import pytest
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_button, find_select_thing
from mini_game_engine.engine.lib import HumanListener, RandomModeGracefulExit
from main_game.models import Creature
from unittest.mock import patch


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
    def human_player(self, app):
        player = app.create_player("human_player")
        player.creatures = [
            Creature.from_prototype_id("bubwool"),
            Creature.from_prototype_id("dumbird")
        ]
        player.active_creature = player.creatures[0]
        return player

    @pytest.fixture
    def bot_player(self, app):
        bot = app.create_bot("basic_opponent")
        bot.creatures = [
            Creature.from_prototype_id("scizard"),
            Creature.from_prototype_id("dumbird")
        ]
        bot.active_creature = bot.creatures[0]
        return bot

    def test_main_game_scene_full_playthrough(self, app, human_player, bot_player):
        scene = MainGameScene(app, human_player)
        scene.bot = bot_player
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        # Human player chooses "Attack"
        choices = runner.dequeue_wait_for_choice(human_player)
        attack_choice = find_button(choices, "Attack")
        runner.make_choice(attack_choice)

        # Human player chooses "Tackle" skill
        choices = runner.dequeue_wait_for_choice(human_player)
        tackle_choice = find_select_thing(choices, "tackle")
        runner.make_choice(tackle_choice)

        # Bot opponent chooses "Attack"
        choices = runner.dequeue_wait_for_choice(bot_player)
        attack_choice = find_button(choices, "Attack")
        runner.make_choice(attack_choice)

        # Bot opponent chooses "Fireball" skill
        choices = runner.dequeue_wait_for_choice(bot_player)
        fireball_choice = find_select_thing(choices, "fireball")
        runner.make_choice(fireball_choice)

        # Resolution phase occurs (Bubwool should go first due to higher speed)
        assert scene.bot.active_creature.hp < scene.bot.active_creature.max_hp
        assert scene.player.active_creature.hp < scene.player.active_creature.max_hp

        # Human player chooses "Attack"
        choices = runner.dequeue_wait_for_choice(human_player)
        attack_choice = find_button(choices, "Attack")
        runner.make_choice(attack_choice)

        # Human player chooses "Lick" skill
        choices = runner.dequeue_wait_for_choice(human_player)
        lick_choice = find_select_thing(choices, "lick")
        runner.make_choice(lick_choice)

        # Bot opponent chooses "Swap"
        choices = runner.dequeue_wait_for_choice(bot_player)
        swap_choice = find_button(choices, "Swap")
        runner.make_choice(swap_choice)

        # Bot opponent swaps to Dumbird
        choices = runner.dequeue_wait_for_choice(bot_player)
        dumbird_choice = find_select_thing(choices, "dumbird")
        runner.make_choice(dumbird_choice)

        # Resolution phase occurs (Swap happens first, then Lick is used)
        assert scene.bot.active_creature.prototype_id == "dumbird"
        assert scene.bot.active_creature.hp < scene.bot.active_creature.max_hp

        # Human player chooses "Swap"
        choices = runner.dequeue_wait_for_choice(human_player)
        swap_choice = find_button(choices, "Swap")
        runner.make_choice(swap_choice)

        # Human player swaps to Dumbird
        choices = runner.dequeue_wait_for_choice(human_player)
        dumbird_choice = find_select_thing(choices, "dumbird")
        runner.make_choice(dumbird_choice)

        # Bot opponent chooses "Attack"
        choices = runner.dequeue_wait_for_choice(bot_player)
        attack_choice = find_button(choices, "Attack")
        runner.make_choice(attack_choice)

        # Bot opponent chooses "Tackle" skill
        choices = runner.dequeue_wait_for_choice(bot_player)
        tackle_choice = find_select_thing(choices, "tackle")
        runner.make_choice(tackle_choice)

        # Resolution phase occurs (Swap happens first, then Tackle is used)
        assert scene.player.active_creature.prototype_id == "dumbird"
        assert scene.player.active_creature.hp < scene.player.active_creature.max_hp

        # Continue the battle until one player has no more creatures
        while True:
            # Human player chooses "Attack"
            choices = runner.dequeue_wait_for_choice(human_player)
            attack_choice = find_button(choices, "Attack")
            runner.make_choice(attack_choice)

            # Human player chooses "Tackle" skill
            choices = runner.dequeue_wait_for_choice(human_player)
            tackle_choice = find_select_thing(choices, "tackle")
            runner.make_choice(tackle_choice)

            # Bot opponent chooses "Attack"
            choices = runner.dequeue_wait_for_choice(bot_player)
            attack_choice = find_button(choices, "Attack")
            runner.make_choice(attack_choice)

            # Bot opponent chooses "Tackle" skill
            choices = runner.dequeue_wait_for_choice(bot_player)
            tackle_choice = find_select_thing(choices, "tackle")
            runner.make_choice(tackle_choice)

            # Check if any player has no more creatures
            if all(c.hp == 0 for c in scene.player.creatures) or all(c.hp == 0 for c in scene.bot.creatures):
                break

            # If a creature faints, force swap
            if scene.player.active_creature.hp == 0:
                choices = runner.dequeue_wait_for_choice(human_player)
                swap_choice = find_select_thing(choices, "bubwool")
                runner.make_choice(swap_choice)

            if scene.bot.active_creature.hp == 0:
                choices = runner.dequeue_wait_for_choice(bot_player)
                swap_choice = find_select_thing(choices, "scizard")
                runner.make_choice(swap_choice)

        # Battle ends, transition to MainMenuScene
        assert runner.dequeue_transition_to_scene() == "MainMenuScene"
