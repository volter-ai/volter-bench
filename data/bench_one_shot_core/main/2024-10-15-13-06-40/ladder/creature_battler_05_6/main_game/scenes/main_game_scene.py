from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


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
            self._player_turn(self.player)
            self._player_turn(self.opponent)
            self._resolve_turn()
            if self._check_battle_end():
                break
        self._end_battle()

    def _initialize_battle(self):
        if not self.player.active_creature:
            self.player.active_creature = self.player.creatures[0]
        if not self.opponent.active_creature:
            self.opponent.active_creature = self.opponent.creatures[0]

    def _player_turn(self, player):
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

    def _choose_skill(self, player):
        skills = player.active_creature.skills
        choices = [SelectThing(skill, label=skill.display_name) for skill in skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _choose_swap_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature, label=creature.display_name) for creature in available_creatures]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _resolve_turn(self):
        # Sort the turn queue, handling speed ties randomly
        self.turn_queue.sort(key=lambda x: (x[1] != "swap", -x[0].active_creature.speed, random.random()))
        for player, action, target in self.turn_queue:
            if action == "swap":
                self._perform_swap(player, target)
            elif action == "attack":
                self._perform_attack(player, target)
                self._check_and_force_swap(self.player)
                self._check_and_force_swap(self.opponent)
        self.turn_queue.clear()

    def _perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_factor)

    def _get_type_factor(self, skill_type, creature_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, creature_type), 1)

    def _check_and_force_swap(self, player):
        if player.active_creature.hp == 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if available_creatures:
                new_creature = self._choose_swap_creature(player)
                if new_creature:
                    self._perform_swap(player, new_creature)
                else:
                    # If the player doesn't choose, force swap to the first available creature
                    self._perform_swap(player, available_creatures[0])
            else:
                self._show_text(player, f"{player.display_name} has no more creatures left!")

    def _check_battle_end(self):
        for player in [self.player, self.opponent]:
            if all(creature.hp == 0 for creature in player.creatures):
                self._show_text(player, f"{player.display_name} has no more creatures left!")
                return True
        return False

    def _end_battle(self):
        winner = self.player if any(c.hp > 0 for c in self.player.creatures) else self.opponent
        self._show_text(self.player, f"{winner.display_name} wins the battle!")
        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
