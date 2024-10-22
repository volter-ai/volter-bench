import random

from main_game.models import Creature, Player, Skill
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.turn_order = [self.player, self.bot]
        random.shuffle(self.turn_order)

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name if player_creature else 'No active creature'}: HP {player_creature.hp}/{player_creature.max_hp if player_creature else 0}
{self.bot.display_name}'s {bot_creature.display_name if bot_creature else 'No active creature'}: HP {bot_creature.hp}/{bot_creature.max_hp if bot_creature else 0}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while True:
            actions = []
            for current_player in self.turn_order:
                action = self._player_turn(current_player)
                if action:
                    actions.append((current_player, action))

            if self._resolve_turn(actions) == "end_battle":
                return

    def _initialize_battle(self):
        for player in [self.player, self.bot]:
            if not player.active_creature and player.creatures:
                player.active_creature = player.creatures[0]

    def _player_turn(self, player: Player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if choice == attack_button:
                skill = self._choose_skill(player)
                if skill:
                    return ("attack", skill)
            elif choice == swap_button:
                new_creature = self._choose_swap_creature(player)
                if new_creature:
                    return ("swap", new_creature)

    def _choose_skill(self, player: Player):
        skills = player.active_creature.skills
        skill_choices = [SelectThing(skill) for skill in skills]
        back_button = Button("Back")
        choices = skill_choices + [back_button]
        choice = self._wait_for_choice(player, choices)

        if choice == back_button:
            return None
        return choice.thing

    def _choose_swap_creature(self, player: Player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices = creature_choices + [back_button]
        choice = self._wait_for_choice(player, choices)

        if choice == back_button:
            return None
        return choice.thing

    def _resolve_turn(self, actions):
        # Separate swap and attack actions
        swap_actions = [action for action in actions if action[1][0] == "swap"]
        attack_actions = [action for action in actions if action[1][0] == "attack"]

        # Resolve swap actions first
        for player, (_, new_creature) in swap_actions:
            self._perform_swap(player, new_creature)

        # Sort attack actions by speed and resolve them
        attack_actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        speed_groups = {}
        for action in attack_actions:
            speed = action[0].active_creature.speed
            if speed not in speed_groups:
                speed_groups[speed] = []
            speed_groups[speed].append(action)

        for speed_group in speed_groups.values():
            random.shuffle(speed_group)
            for player, (_, skill) in speed_group:
                self._perform_attack(player, skill)
                if self._check_battle_end():
                    return "end_battle"
                self._force_swap_if_needed(player)
                self._force_swap_if_needed(self._get_opponent(player))

        return "continue"

    def _perform_swap(self, player: Player, new_creature: Creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker: Player, skill: Skill):
        defender = self._get_opponent(attacker)
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        return max(1, final_damage)

    def _get_type_factor(self, skill_type: str, defender_type: str):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _check_battle_end(self):
        for player in [self.player, self.bot]:
            if all(creature.hp == 0 for creature in player.creatures):
                winner = self._get_opponent(player)
                self._show_text(self.player, f"{winner.display_name} wins the battle!")
                self._transition_to_scene("MainMenuScene")
                return True
        return False

    def _force_swap_if_needed(self, player: Player):
        if player.active_creature.hp == 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if available_creatures:
                new_creature = available_creatures[0]
                self._perform_swap(player, new_creature)
            else:
                self._show_text(player, f"{player.display_name} has no more creatures able to battle!")

    def _get_opponent(self, player: Player):
        return self.bot if player == self.player else self.player
