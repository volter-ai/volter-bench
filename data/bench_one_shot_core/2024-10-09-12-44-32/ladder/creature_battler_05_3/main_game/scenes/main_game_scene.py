import random

from main_game.models import Player
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.turn_queue = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player.active_creature.display_name}: HP {self.player.active_creature.hp}/{self.player.active_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        self.game_loop()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]

    def game_loop(self):
        while True:
            self._player_choice_phase(self.player)
            self._foe_choice_phase()
            self._resolution_phase()

            if self._check_battle_end():
                break

        self._end_battle()

    def _player_choice_phase(self, player):
        self._notify_opponent_waiting(player)
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if attack_button == choice:
                skill = self._choose_skill(player)
                if skill:
                    self.turn_queue.append((player, "attack", skill))
                    break
            elif swap_button == choice:
                new_creature = self._choose_swap_creature(player)
                if new_creature:
                    self.turn_queue.append((player, "swap", new_creature))
                    break

    def _foe_choice_phase(self):
        # In a real multiplayer scenario, this would be another player's turn
        # For this implementation, we'll simulate a simple AI choice
        foe = Player.from_prototype_id("basic_opponent")
        foe.active_creature = foe.creatures[0]
        skill = random.choice(foe.active_creature.skills)
        self.turn_queue.append((foe, "attack", skill))

    def _notify_opponent_waiting(self, active_player):
        # In a real multiplayer scenario, this would notify the other player
        pass

    def _choose_skill(self, player):
        skills = player.active_creature.skills
        choices = [SelectThing(skill) for skill in skills] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, SelectThing):
            return choice.thing
        return None

    def _choose_swap_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, SelectThing):
            return choice.thing
        return None

    def _resolution_phase(self):
        self.turn_queue.sort(key=lambda x: (x[1] != "swap", -x[0].active_creature.speed))
        
        for player, action_type, action in self.turn_queue:
            if action_type == "swap":
                self._perform_swap(player, action)
            elif action_type == "attack":
                self._perform_attack(player, action)
                self._check_and_handle_fainted_creature(player)

        self.turn_queue.clear()

    def _perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker, skill):
        defender = self.player if attacker != self.player else Player.from_prototype_id("basic_opponent")
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)

    def _get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("water", "fire"): 2,
            ("leaf", "water"): 2,
            ("fire", "water"): 0.5,
            ("water", "leaf"): 0.5,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def _check_and_handle_fainted_creature(self, player):
        if player.active_creature.hp == 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if available_creatures:
                self._show_text(player, f"{player.active_creature.display_name} has fainted!")
                new_creature = self._force_swap_creature(player, available_creatures)
                self._perform_swap(player, new_creature)
            else:
                self._show_text(player, f"{player.display_name} has no more creatures able to battle!")

    def _force_swap_creature(self, player, available_creatures):
        choices = [SelectThing(creature) for creature in available_creatures]
        self._show_text(player, "Choose a creature to swap in:")
        choice = self._wait_for_choice(player, choices)
        return choice.thing

    def _check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        foe = Player.from_prototype_id("basic_opponent")
        if all(creature.hp == 0 for creature in foe.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _end_battle(self):
        self._transition_to_scene("MainMenuScene")
