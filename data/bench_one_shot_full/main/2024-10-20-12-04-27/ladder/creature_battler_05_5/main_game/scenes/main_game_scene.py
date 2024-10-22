from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random
from functools import cmp_to_key


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.turn_counter = 0

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""===Battle===
Turn: {self.turn_counter}

{self.player.display_name}'s {player_creature.display_name}:
HP: {player_creature.hp}/{player_creature.max_hp}

{self.opponent.display_name}'s {opponent_creature.display_name}:
HP: {opponent_creature.hp}/{opponent_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while True:
            self.turn_counter += 1
            player_action = self._player_choice_phase(self.player)
            opponent_action = self._player_choice_phase(self.opponent)
            self._resolution_phase(player_action, opponent_action)
            
            winner = self._check_battle_end()
            if winner:
                self._show_text(self.player, f"{winner.display_name} wins the battle!")
                self._show_text(self.opponent, f"{winner.display_name} wins the battle!")
                play_again = self._ask_play_again()
                self._reset_creatures_state()
                if play_again:
                    self._transition_to_scene("MainMenuScene")
                else:
                    self._quit_whole_game()
                return

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def _player_choice_phase(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if attack_button == choice:
                action = self._choose_attack(player)
                if action:
                    return action
            elif swap_button == choice:
                action = self._choose_swap(player)
                if action:
                    return action

    def _choose_attack(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices.append(back_button)
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return None
        return choice

    def _choose_swap(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        if not available_creatures:
            self._show_text(player, "No creatures available to swap.")
            return None
        choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices.append(back_button)
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return None
        return choice

    def _resolution_phase(self, player_action, opponent_action):
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]
        
        def compare_actions(a, b):
            a_player, a_action = a
            b_player, b_action = b
            
            # Swap actions always go first
            if isinstance(a_action.thing, Creature) and not isinstance(b_action.thing, Creature):
                return -1
            if isinstance(b_action.thing, Creature) and not isinstance(a_action.thing, Creature):
                return 1
            
            # Compare speeds
            a_speed = a_player.active_creature.speed
            b_speed = b_player.active_creature.speed
            if a_speed > b_speed:
                return -1
            elif a_speed < b_speed:
                return 1
            else:
                # If speeds are tied, return a random result
                return random.choice([-1, 1])

        # Sort actions using the custom comparison function
        actions.sort(key=cmp_to_key(compare_actions))

        for actor, action in actions:
            if isinstance(action.thing, Creature):
                self._perform_swap(actor, action.thing)
            elif isinstance(action.thing, Skill):
                self._perform_attack(actor, action.thing)

            # Check if the active creature fainted and force a swap if necessary
            if actor.active_creature.hp <= 0:
                if not self._force_swap(actor):
                    # If no creatures are available to swap, the battle ends
                    return

    def _perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def _get_type_effectiveness(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def _check_battle_end(self):
        for player in [self.player, self.opponent]:
            if all(creature.hp <= 0 for creature in player.creatures):
                return self.opponent if player == self.player else self.player
        return None

    def _force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return False
        choices = [SelectThing(creature) for creature in available_creatures]
        new_creature = self._wait_for_choice(player, choices).thing
        self._perform_swap(player, new_creature)
        return True

    def _ask_play_again(self):
        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choices = [play_again_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)
        return choice == play_again_button

    def _reset_creatures_state(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
        self.player.active_creature = None
        self.opponent.active_creature = None
