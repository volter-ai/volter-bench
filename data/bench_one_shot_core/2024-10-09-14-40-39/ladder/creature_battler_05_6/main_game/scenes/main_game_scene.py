import random

from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.turn_queue = []

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name if player_creature else 'No active creature'}: HP {player_creature.hp}/{player_creature.max_hp if player_creature else 0}
{self.opponent.display_name}'s {opponent_creature.display_name if opponent_creature else 'No active creature'}: HP {opponent_creature.hp}/{opponent_creature.max_hp if opponent_creature else 0}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while True:
            self._player_choice_phase(self.player)
            self._player_choice_phase(self.opponent)
            self._resolution_phase()
            if self._check_battle_end():
                break
        self._end_battle()

    def _initialize_battle(self):
        if not self.player.active_creature and self.player.creatures:
            self.player.active_creature = self.player.creatures[0]
        if not self.opponent.active_creature and self.opponent.creatures:
            self.opponent.active_creature = self.opponent.creatures[0]

    def _player_choice_phase(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if choice == attack_button:
                skill = self._choose_skill(player)
                if skill:
                    self.turn_queue.append((player, "attack", skill))
                    break
            elif choice == swap_button:
                new_creature = self._choose_swap_creature(player)
                if new_creature:
                    self.turn_queue.append((player, "swap", new_creature))
                    break

    def _choose_skill(self, player):
        skills = player.active_creature.skills
        choices = [SelectThing(skill) for skill in skills] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _choose_swap_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _resolution_phase(self):
        # Sort by action type (swap first), then by speed with a random factor for equal speeds
        self.turn_queue.sort(key=lambda x: (x[1] != "swap", -x[0].active_creature.speed, random.random()))
        
        while self.turn_queue:
            player, action_type, action = self.turn_queue.pop(0)
            opponent = self.opponent if player == self.player else self.player

            if action_type == "swap":
                old_creature = player.active_creature
                player.active_creature = action
                self._show_text(player, f"{player.display_name} swapped {old_creature.display_name} for {action.display_name}!")
                
                # Execute any queued attacks against the swapped-in creature
                opponent_attacks = [a for a in self.turn_queue if a[0] == opponent and a[1] == "attack"]
                for attack in opponent_attacks:
                    self._execute_attack(opponent, attack[2])
                    self.turn_queue.remove(attack)
                    if self._check_battle_end():
                        return

            elif action_type == "attack":
                self._execute_attack(player, action)
                if self._check_battle_end():
                    return

            # Check for forced swap after each action
            if not self._force_swap(self.player) or not self._force_swap(self.opponent):
                return  # End battle if forced swap is not possible

    def _execute_attack(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        type_factor = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_factor)  # Explicitly convert to integer

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

    def _force_swap(self, player):
        if player.active_creature.hp == 0:
            available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
            if not available_creatures:
                self._show_text(player, f"{player.display_name} has no more creatures able to battle!")
                return False
            new_creature = available_creatures[0]  # Choose the first available creature
            player.active_creature = new_creature
            self._show_text(player, f"{player.display_name} was forced to swap to {new_creature.display_name}!")
        return True

    def _check_battle_end(self):
        for player in [self.player, self.opponent]:
            if all(creature.hp == 0 for creature in player.creatures):
                winner = self.opponent if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins the battle!")
                return True
        return False

    def _end_battle(self):
        # Reset all creatures' HP to their max HP
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
        self._transition_to_scene("MainMenuScene")
