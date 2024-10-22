import random

from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.turn_counter = 0

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        return f"""===Battle===
Turn: {self.turn_counter}

{self.player.display_name}'s {player_creature.display_name}:
HP: {player_creature.hp}/{player_creature.max_hp}

{self.bot.display_name}'s {bot_creature.display_name}:
HP: {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while True:
            self.turn_counter += 1
            player_action = self._player_choice_phase(self.player)
            bot_action = self._player_choice_phase(self.bot)
            self._resolution_phase(player_action, bot_action)
            
            if self._check_battle_end():
                break
        
        self._reset_creature_states()
        self._transition_to_scene("MainMenuScene")

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def _player_choice_phase(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if choice == attack_button:
                return self._choose_attack(current_player)
            elif choice == swap_button:
                return self._choose_swap(current_player)

    def _choose_attack(self, current_player):
        skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
        back_button = Button("Back")
        choices = skill_choices + [back_button]
        choice = self._wait_for_choice(current_player, choices)

        if choice == back_button:
            return self._player_choice_phase(current_player)
        return ("attack", choice.thing)

    def _choose_swap(self, current_player):
        available_creatures = [creature for creature in current_player.creatures 
                               if creature != current_player.active_creature and creature.hp > 0]
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices = creature_choices + [back_button]
        choice = self._wait_for_choice(current_player, choices)

        if choice == back_button:
            return self._player_choice_phase(current_player)
        return ("swap", choice.thing)

    def _resolution_phase(self, player_action, bot_action):
        actions = [
            (self.player, player_action),
            (self.bot, bot_action)
        ]
        
        # Sort actions: swaps first, then by speed (with random tie-breaker)
        actions.sort(key=lambda x: (x[1][0] != "swap", -x[0].active_creature.speed, random.random()))

        for current_player, action in actions:
            if action[0] == "swap":
                self._perform_swap(current_player, action[1])
            elif action[0] == "attack":
                self._perform_attack(current_player, action[1])

    def _perform_swap(self, current_player, new_creature):
        current_player.active_creature = new_creature
        self._show_text(self.player, f"{current_player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} took {damage} damage!")

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        else:
            raw_damage = float(attacker.sp_attack) / float(defender.sp_defense) * float(skill.base_damage)

        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def _get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1.0)

    def _check_battle_end(self):
        player_alive_creatures = [c for c in self.player.creatures if c.hp > 0]
        bot_alive_creatures = [c for c in self.bot.creatures if c.hp > 0]

        if not player_alive_creatures:
            self._show_text(self.player, f"{self.bot.display_name} wins the battle!")
            return True
        elif not bot_alive_creatures:
            self._show_text(self.player, f"{self.player.display_name} wins the battle!")
            return True

        if self.player.active_creature.hp == 0:
            self._force_swap(self.player)
        if self.bot.active_creature.hp == 0:
            self._force_swap(self.bot)

        return False

    def _force_swap(self, current_player):
        available_creatures = [c for c in current_player.creatures if c.hp > 0]
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        self._show_text(self.player, f"{current_player.display_name}'s {current_player.active_creature.display_name} was knocked out!")
        choice = self._wait_for_choice(current_player, creature_choices)
        self._perform_swap(current_player, choice.thing)

    def _reset_creature_states(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
