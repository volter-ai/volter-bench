import random
from itertools import groupby

from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.turn_queue = []

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.opponent.display_name}'s {opponent_creature.display_name}: HP {opponent_creature.hp}/{opponent_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while True:
            self._player_turn()
            self._opponent_turn()
            self._resolve_turn()
            if self._check_battle_end():
                break
        self._end_battle()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def _player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if attack_button == choice:
                skill = self._choose_skill(self.player)
                if skill:
                    self.turn_queue.append(("attack", self.player, skill))
                    break
            elif swap_button == choice:
                new_creature = self._choose_creature(self.player)
                if new_creature:
                    self.turn_queue.append(("swap", self.player, new_creature))
                    break

    def _opponent_turn(self):
        choice = self._wait_for_choice(self.opponent, [Button("Attack"), Button("Swap")])
        if choice.display_name == "Attack":
            skill = self._choose_skill(self.opponent)
            if skill:
                self.turn_queue.append(("attack", self.opponent, skill))
            else:
                # If no skill was chosen, force a swap
                new_creature = self._choose_creature(self.opponent)
                if new_creature:
                    self.turn_queue.append(("swap", self.opponent, new_creature))
        else:
            new_creature = self._choose_creature(self.opponent)
            if new_creature:
                self.turn_queue.append(("swap", self.opponent, new_creature))

    def _choose_skill(self, player):
        skills = player.active_creature.skills
        choices = [SelectThing(skill) for skill in skills] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _choose_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        if not available_creatures:
            self._show_text(player, "No other creatures available to swap!")
            return None
        choices = [SelectThing(creature) for creature in available_creatures] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _resolve_turn(self):
        # Sort actions by speed, with swaps always going first
        sorted_actions = sorted(self.turn_queue, key=lambda x: (-1 if x[0] == "swap" else x[1].active_creature.speed), reverse=True)
        
        # Group actions by speed
        speed_groups = groupby(sorted_actions, key=lambda x: -1 if x[0] == "swap" else x[1].active_creature.speed)
        
        # Shuffle actions within each speed group and execute
        for _, group in speed_groups:
            actions = list(group)
            random.shuffle(actions)
            for action, player, target in actions:
                if action == "swap":
                    if target is not None:
                        player.active_creature = target
                        self._show_text(player, f"{player.display_name} swapped to {target.display_name}!")
                    else:
                        self._show_text(player, f"{player.display_name} failed to swap creatures.")
                elif action == "attack":
                    if target is not None:
                        self._execute_skill(player, target)
                    else:
                        self._show_text(player, f"{player.display_name} failed to execute a skill.")
        
        self.turn_queue.clear()

    def _execute_skill(self, attacker, skill):
        if skill is None:
            self._show_text(attacker, f"{attacker.display_name} failed to execute a skill.")
            return

        defender = self.player if attacker == self.opponent else self.opponent
        defender_creature = defender.active_creature
        
        if skill.is_physical:
            raw_damage = float(attacker.active_creature.attack) + float(skill.base_damage) - float(defender_creature.defense)
        else:
            raw_damage = (float(attacker.active_creature.sp_attack) / float(defender_creature.sp_defense)) * float(skill.base_damage)
        
        weakness_factor = self._calculate_weakness(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {final_damage} damage!")
        
        if defender_creature.hp == 0:
            self._show_text(defender, f"{defender_creature.display_name} was knocked out!")
            self._force_swap(defender)

    def _calculate_weakness(self, skill_type, defender_type):
        weaknesses = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return weaknesses.get(skill_type, {}).get(defender_type, 1.0)

    def _force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        else:
            self._show_text(player, f"{player.display_name} has no more creatures able to battle!")

    def _check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _end_battle(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
        self._transition_to_scene("MainMenuScene")
