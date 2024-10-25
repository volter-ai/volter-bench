from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
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
        while True:
            if self._is_battle_over():
                break
            self._player_choice_phase(self.player)
            self._player_choice_phase(self.bot)
            self._resolution_phase()

        self._end_battle()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def _is_battle_over(self):
        return all(c.hp <= 0 for c in self.player.creatures) or all(c.hp <= 0 for c in self.bot.creatures)

    def _player_choice_phase(self, player):
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
        choices = [SelectThing(skill) for skill in skills] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _choose_swap_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _resolution_phase(self):
        # Prioritize swap actions
        swap_actions = [action for action in self.turn_queue if action[1] == "swap"]
        attack_actions = [action for action in self.turn_queue if action[1] == "attack"]

        # Perform swap actions first
        for action in swap_actions:
            player, _, new_creature = action
            self._perform_swap(player, new_creature)

        # Sort attack actions by creature speed
        attack_actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)

        # Resolve equal speed randomly
        i = 0
        while i < len(attack_actions) - 1:
            if attack_actions[i][0].active_creature.speed == attack_actions[i+1][0].active_creature.speed:
                if random.random() < 0.5:
                    attack_actions[i], attack_actions[i+1] = attack_actions[i+1], attack_actions[i]
            i += 1

        # Perform attack actions
        for action in attack_actions:
            player, _, skill = action
            self._perform_attack(player, skill)

        self.turn_queue.clear()

    def _perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        defender_creature = defender.active_creature
        
        damage = self._calculate_damage(attacker.active_creature, defender_creature, skill)
        defender_creature.hp = max(0, defender_creature.hp - damage)

        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender_creature.display_name} took {damage} damage!")

        if defender_creature.hp == 0:
            self._show_text(defender, f"{defender_creature.display_name} was knocked out!")
            self._force_swap(defender)

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        else:
            raw_damage = float((attacker.sp_attack / defender.sp_defense) * skill.base_damage)

        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_factor)  # Explicitly convert to integer

    def _get_type_factor(self, skill_type, defender_type):
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
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, choices)
            self._perform_swap(player, choice.thing)

    def _end_battle(self):
        winner = self.player if any(c.hp > 0 for c in self.player.creatures) else self.bot
        self._show_text(self.player, f"{winner.display_name} wins the battle!")
        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _reset_creatures(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
