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

{self.player.display_name}'s {player_creature.display_name}
HP: {player_creature.hp}/{player_creature.max_hp}

{self.opponent.display_name}'s {opponent_creature.display_name}
HP: {opponent_creature.hp}/{opponent_creature.max_hp}

> Attack
> Swap (if available)
"""

    def run(self):
        self._initialize_battle()
        while True:
            self.turn_counter += 1
            player_action = self._player_choice_phase(self.player)
            opponent_action = self._player_choice_phase(self.opponent)
            self._resolution_phase(player_action, opponent_action)
            
            if self._check_battle_end():
                self._end_battle()
                return  # Exit the run method after ending the battle

    def _initialize_battle(self):
        if not self.player.active_creature and self.player.creatures:
            self.player.active_creature = self.player.creatures[0]
        if not self.opponent.active_creature and self.opponent.creatures:
            self.opponent.active_creature = self.opponent.creatures[0]

    def _player_choice_phase(self, player):
        while True:
            attack_button = Button("Attack")
            choices = [attack_button]
            
            if self._has_available_creatures_to_swap(player):
                swap_button = Button("Swap")
                choices.append(swap_button)
            
            choice = self._wait_for_choice(player, choices)

            if attack_button == choice:
                action = self._choose_attack(player)
            elif choice == Button("Swap"):
                action = self._choose_swap(player)
            else:
                continue

            if action:
                return action

    def _choose_attack(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return choice

    def _choose_swap(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return choice

    def _has_available_creatures_to_swap(self, player):
        return any(c != player.active_creature and c.hp > 0 for c in player.creatures)

    def _get_action_priority(self, player, action):
        is_swap = isinstance(action.thing, Creature)
        speed = player.active_creature.speed
        return (is_swap, -speed, random.random())

    def _resolution_phase(self, player_action, opponent_action):
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]
        
        # Sort actions based on priority (swap first, then speed, then random)
        actions.sort(key=lambda x: self._get_action_priority(x[0], x[1]))

        for player, action in actions:
            if isinstance(action.thing, Creature):
                self._perform_swap(player, action.thing)
            elif isinstance(action.thing, Skill):
                self._perform_attack(player, action.thing)
            
            # Check if the opponent's creature is knocked out and force a swap if necessary
            opponent = self.opponent if player == self.player else self.player
            if opponent.active_creature.hp == 0:
                self._force_swap(opponent)

    def _perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker, skill):
        defender = self.opponent if attacker == self.player else self.player
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def _force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return  # No available creatures, battle will end in the next check

        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        if len(available_creatures) == 1:
            new_creature = available_creatures[0]
        else:
            choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, choices)
            new_creature = choice.thing

        self._perform_swap(player, new_creature)

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
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
        player_defeated = all(c.hp == 0 for c in self.player.creatures)
        opponent_defeated = all(c.hp == 0 for c in self.opponent.creatures)
        
        if player_defeated:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif opponent_defeated:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _end_battle(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
        self._transition_to_scene("MainMenuScene")
