import pytest
from main_game.main import App
from main_game.scenes.main_game_scene import MainGameScene
from mini_game_engine.engine.lib import HumanListener, AbstractApp
from mini_game_engine.engine.qa_utils import ThreadedSceneRunner, find_select_thing, find_button


@pytest.fixture
def app():
    return App()

def test_main_game_scene(app):
    HumanListener.random_mode = True
    player = app.create_player("test_player")
    
    for _ in range(10):
        try:
            app.transition_to_scene("MainGameScene", player=player)
        except AbstractApp._QuitWholeGame:
            # This exception is expected when the game ends gracefully
            break

class TestMainGameScene:
    @pytest.fixture
    def player(self, app):
        player = app.create_player("test_player")
        player.display_name = "Player 1"
        return player

    @pytest.fixture
    def opponent(self, app):
        opponent = app.create_bot("basic_opponent")
        opponent.display_name = "Player 2"
        return opponent

    def handle_initial_setup(self, runner, player, opponent):
        # Handle player's initial turn
        choices = runner.dequeue_wait_for_choice(player)
        attack_choice = find_button(choices, "Attack")
        runner.make_choice(attack_choice)

        choices = runner.dequeue_wait_for_choice(player)
        skill_choice = find_select_thing(choices, "tackle")
        runner.make_choice(skill_choice)

        # Handle opponent's initial turn
        choices = runner.dequeue_wait_for_choice(opponent)
        attack_choice = find_button(choices, "Attack")
        runner.make_choice(attack_choice)

        choices = runner.dequeue_wait_for_choice(opponent)
        skill_choice = find_select_thing(choices, "tackle")
        runner.make_choice(skill_choice)

        # Handle random speed tie-breaker
        random_call = runner.dequeue_random_call()
        assert random_call['function'] == 'shuffle'

    def test_player_wins_battle(self, app, player, opponent):
        scene = MainGameScene(app, player)
        scene.opponent = opponent
        
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        self.handle_initial_setup(runner, player, opponent)

        for _ in range(5):  # Reduced to 5 rounds as we've already handled the initial setup
            # Player's turn
            choices = runner.dequeue_wait_for_choice(player)
            attack_choice = find_button(choices, "Attack")
            runner.make_choice(attack_choice)

            choices = runner.dequeue_wait_for_choice(player)
            skill_choice = find_select_thing(choices, "tackle")
            runner.make_choice(skill_choice)

            # Opponent's turn
            choices = runner.dequeue_wait_for_choice(opponent)
            attack_choice = find_button(choices, "Attack")
            runner.make_choice(attack_choice)

            choices = runner.dequeue_wait_for_choice(opponent)
            skill_choice = find_select_thing(choices, "tackle")
            runner.make_choice(skill_choice)

            # Handle random speed tie-breaker
            random_call = runner.dequeue_random_call()
            assert random_call['function'] == 'shuffle'

        # Check game state after the battle
        assert all(creature.hp == 0 for creature in opponent.creatures)
        assert any(creature.hp > 0 for creature in player.creatures)
        assert runner.dequeue_transition_to_scene() == "MainMenuScene"

    def test_player_swaps_creature(self, app, player, opponent):
        scene = MainGameScene(app, player)
        scene.opponent = opponent
        
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        self.handle_initial_setup(runner, player, opponent)

        # Player's turn - Swap creature
        choices = runner.dequeue_wait_for_choice(player)
        swap_choice = find_button(choices, "Swap")
        runner.make_choice(swap_choice)

        choices = runner.dequeue_wait_for_choice(player)
        new_creature = find_select_thing(choices, "dumbird")
        runner.make_choice(new_creature)

        # Opponent's turn
        choices = runner.dequeue_wait_for_choice(opponent)
        attack_choice = find_button(choices, "Attack")
        runner.make_choice(attack_choice)

        choices = runner.dequeue_wait_for_choice(opponent)
        skill_choice = find_select_thing(choices, "tackle")
        runner.make_choice(skill_choice)

        # Handle random speed tie-breaker
        random_call = runner.dequeue_random_call()
        assert random_call['function'] == 'shuffle'

        assert player.active_creature.prototype_id == "dumbird"
        assert runner.dequeue_transition_to_scene() == "MainMenuScene"

    def test_forced_swap_after_knockout(self, app, player, opponent):
        scene = MainGameScene(app, player)
        scene.opponent = opponent
        
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        self.handle_initial_setup(runner, player, opponent)

        # Set player's active creature HP to 1 for quick knockout
        player.active_creature.hp = 1

        # Player's turn
        choices = runner.dequeue_wait_for_choice(player)
        attack_choice = find_button(choices, "Attack")
        runner.make_choice(attack_choice)

        choices = runner.dequeue_wait_for_choice(player)
        skill_choice = find_select_thing(choices, "tackle")
        runner.make_choice(skill_choice)

        # Opponent's turn - will knock out player's active creature
        choices = runner.dequeue_wait_for_choice(opponent)
        attack_choice = find_button(choices, "Attack")
        runner.make_choice(attack_choice)

        choices = runner.dequeue_wait_for_choice(opponent)
        skill_choice = find_select_thing(choices, "tackle")
        runner.make_choice(skill_choice)

        # Handle random speed tie-breaker
        random_call = runner.dequeue_random_call()
        assert random_call['function'] == 'shuffle'

        # Player forced to swap
        choices = runner.dequeue_wait_for_choice(player)
        new_creature = find_select_thing(choices, "dumbird")
        runner.make_choice(new_creature)

        assert player.active_creature.prototype_id == "dumbird"
        assert player.creatures[0].hp == 0
        assert runner.dequeue_transition_to_scene() == "MainMenuScene"

    def test_type_effectiveness(self, app, player, opponent):
        scene = MainGameScene(app, player)
        scene.opponent = opponent
        
        runner = ThreadedSceneRunner()
        runner.start_game(scene)

        self.handle_initial_setup(runner, player, opponent)

        # Set player's active creature to Bubwool (water-type)
        player.active_creature = player.creatures[0]
        
        # Set opponent's active creature to Scizard (fire-type)
        opponent.active_creature = opponent.creatures[0]
        
        initial_hp = opponent.active_creature.hp
        
        # Player's turn - use water-type attack against fire-type
        choices = runner.dequeue_wait_for_choice(player)
        attack_choice = find_button(choices, "Attack")
        runner.make_choice(attack_choice)

        choices = runner.dequeue_wait_for_choice(player)
        skill_choice = find_select_thing(choices, "lick")
        runner.make_choice(skill_choice)

        # Opponent's turn
        choices = runner.dequeue_wait_for_choice(opponent)
        attack_choice = find_button(choices, "Attack")
        runner.make_choice(attack_choice)

        choices = runner.dequeue_wait_for_choice(opponent)
        skill_choice = find_select_thing(choices, "tackle")
        runner.make_choice(skill_choice)

        # Handle random speed tie-breaker
        random_call = runner.dequeue_random_call()
        assert random_call['function'] == 'shuffle'

        # Check that the water-type attack was super effective
        assert opponent.active_creature.hp < initial_hp - 10  # Assuming base damage is more than 5
        assert runner.dequeue_transition_to_scene() == "MainMenuScene"
