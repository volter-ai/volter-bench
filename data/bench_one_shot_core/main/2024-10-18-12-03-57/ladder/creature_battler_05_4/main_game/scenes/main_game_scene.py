from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
        while True:
            self.turn_counter += 1
            
            if not self._has_available_creatures(self.player) or not self._has_available_creatures(self.opponent):
                self._end_battle()
                break

            player_action = self._player_choice_phase(self.player)
            opponent_action = self._player_choice_phase(self.opponent)
            
            if player_action is None or opponent_action is None:
                self._end_battle()
                break

            self._resolution_phase(player_action, opponent_action)
            
            if self._check_battle_end():
                break

        self._reset_creatures_state()
        self._transition_to_scene("MainMenuScene")

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def _player_choice_phase(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            back_button = Button("Back")
            choices = [attack_button, swap_button, back_button]
            choice = self._wait_for_choice(player, choices)

            if attack_button == choice:
                attack_action = self._choose_attack(player)
                if attack_action:
                    return attack_action
            elif swap_button == choice:
                swap_action = self._choose_swap(player)
                if swap_action:
                    return swap_action
            elif back_button == choice:
                continue

    def _choose_attack(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return choice

    def _choose_swap(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        if not available_creatures:
            self._show_text(player, f"{player.display_name} has no available creatures to swap!")
            return None
        choices = [SelectThing(creature) for creature in available_creatures]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button) and choice.display_name == "Back":
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
            -x[0].active_creature.speed,
            random.random()  # Random tiebreaker for same speed
        ))

        for actor, action in actions:
            if isinstance(action.thing, Creature):
                self._perform_swap(actor, action.thing)
            elif isinstance(action.thing, Skill):
                self._perform_attack(actor, action.thing)

            # Check if the defending creature is knocked out and force a swap if necessary
            defender = self.opponent if actor == self.player else self.player
            if defender.active_creature.hp == 0:
                self._force_swap(defender)

    def _perform_swap(self, actor, new_creature):
        actor.active_creature = new_creature
        self._show_text(actor, f"{actor.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker, skill):
        defender = self.opponent if attacker == self.player else self.player
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
        if not self._has_available_creatures(self.player):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not self._has_available_creatures(self.opponent):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _has_available_creatures(self, player):
        return any(c.hp > 0 for c in player.creatures)

    def _force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            new_creature = random.choice(available_creatures)
            self._perform_swap(player, new_creature)
        else:
            self._show_text(player, f"{player.display_name} has no more available creatures!")

    def _end_battle(self):
        if not self._has_available_creatures(self.player):
            self._show_text(self.player, "You lost the battle!")
        elif not self._has_available_creatures(self.opponent):
            self._show_text(self.player, "You won the battle!")
        else:
            self._show_text(self.player, "The battle ended in a draw!")

    def _reset_creatures_state(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
