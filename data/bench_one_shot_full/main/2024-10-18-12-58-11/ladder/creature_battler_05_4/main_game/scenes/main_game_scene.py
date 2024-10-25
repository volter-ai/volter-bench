from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, HumanListener, RandomModeGracefulExit
from main_game.models import Creature, Skill
import random


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
        try:
            while True:
                self.turn_counter += 1
                player_action = self._player_choice_phase(self.player)
                opponent_action = self._player_choice_phase(self.opponent)
                self._resolution_phase(player_action, opponent_action)
                
                if self._check_battle_end():
                    break

                if isinstance(self.player._listener, HumanListener) and self.player._listener.random_mode:
                    self.player._listener.random_mode_counter -= 1
                    if self.player._listener.random_mode_counter <= 0:
                        raise RandomModeGracefulExit()

        except RandomModeGracefulExit:
            print("Random mode gracefully exiting the battle")
        finally:
            self._reset_creatures_state()
            self._transition_to_scene("MainMenuScene")

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
            self._show_text(player, "No creatures available to swap!")
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
        
        # Sort actions based on speed (swap actions go first)
        actions.sort(key=lambda x: (
            isinstance(x[1].thing, Creature),
            -x[0].active_creature.speed
        ))

        # Randomize order for same-speed creatures
        if (isinstance(actions[0][1].thing, Skill) and isinstance(actions[1][1].thing, Skill) and
            actions[0][0].active_creature.speed == actions[1][0].active_creature.speed):
            random.shuffle(actions)

        for actor, action in actions:
            if isinstance(action.thing, Creature):
                self._perform_swap(actor, action.thing)
            elif isinstance(action.thing, Skill):
                self._perform_attack(actor, action.thing)

    def _perform_swap(self, actor, new_creature):
        actor.active_creature = new_creature
        self._show_text(actor, f"{actor.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker, skill):
        defender = self.opponent if attacker == self.player else self.player
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")

        if defender.active_creature.hp == 0:
            self._handle_knocked_out_creature(defender)

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
            if all(c.hp == 0 for c in player.creatures):
                winner = self.opponent if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} won the battle!")
                return True
        return False

    def _handle_knocked_out_creature(self, player):
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            self._force_swap(player)
        else:
            self._show_text(player, f"{player.display_name} has no more creatures available!")

    def _force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures]
        self._show_text(player, "Choose a creature to swap in:")
        new_creature = self._wait_for_choice(player, choices).thing
        self._perform_swap(player, new_creature)

    def _reset_creatures_state(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
        self.player.active_creature = None
        self.opponent.active_creature = None
