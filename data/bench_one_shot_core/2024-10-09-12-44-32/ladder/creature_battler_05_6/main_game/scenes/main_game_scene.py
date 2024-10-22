import random

from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.turn_queue = []

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.bot.display_name}'s {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        self.game_loop()
        self._reset_creatures()  # Reset creatures when leaving the scene

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def game_loop(self):
        while True:
            self._player_choice_phase(self.player)
            self._player_choice_phase(self.bot)
            self._resolution_phase()
            
            if self._check_battle_end():
                break

    def _player_choice_phase(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if attack_button == choice:
                skill = self._choose_skill(current_player)
                if skill:
                    self.turn_queue.append((current_player, "attack", skill))
                    break
            elif swap_button == choice:
                new_creature = self._choose_swap_creature(current_player)
                if new_creature:
                    self.turn_queue.append((current_player, "swap", new_creature))
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
        for player, action_type, action in sorted(self.turn_queue, key=lambda x: self._get_action_priority(x)):
            if action_type == "swap":
                self._perform_swap(player, action)
            elif action_type == "attack":
                self._perform_attack(player, action)

        self.turn_queue.clear()

    def _get_action_priority(self, action_tuple):
        player, action_type, _ = action_tuple
        if action_type == "swap":
            return (-1, 0)  # Swaps always go first
        return (0, -player.active_creature.speed, random.random())  # Attacks are sorted by speed, with a random tiebreaker

    def _perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")
        self._check_knockout(defender)

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_factor)

    def _get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _check_knockout(self, player):
        if player.active_creature.hp == 0:
            self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if available_creatures:
                new_creature = self._force_swap(player, available_creatures)
                player.active_creature = new_creature
                self._show_text(player, f"{player.display_name} sent out {new_creature.display_name}!")
            else:
                self._end_battle(self.player if player == self.bot else self.bot)

    def _force_swap(self, player, available_creatures):
        choices = [SelectThing(creature) for creature in available_creatures]
        return self._wait_for_choice(player, choices).thing

    def _check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._end_battle(self.bot)
            return True
        if all(c.hp == 0 for c in self.bot.creatures):
            self._end_battle(self.player)
            return True
        return False

    def _end_battle(self, winner):
        self._show_text(self.player, f"{winner.display_name} won the battle!")
        self._reset_creatures()  # Reset creatures before transitioning
        self._transition_to_scene("MainMenuScene")

    def _reset_creatures(self):
        for player in [self.player, self.bot]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
