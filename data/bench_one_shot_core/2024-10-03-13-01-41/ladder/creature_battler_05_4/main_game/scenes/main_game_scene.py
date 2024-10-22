import random

from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.turn_count = 0

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        return f"""===Battle===
Turn: {self.turn_count}

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
            self.turn_count += 1
            player_action = self._player_choice_phase(self.player)
            bot_action = self._player_choice_phase(self.bot)
            self._resolution_phase(player_action, bot_action)
            
            if self._check_battle_end():
                break

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
        
        # Sort actions: swaps first, then by speed, with random tiebreaker for equal speeds
        actions.sort(key=lambda x: (x[1][0] != "swap", -x[0].active_creature.speed, random.random()))

        for current_player, action in actions:
            if action[0] == "swap":
                self._perform_swap(current_player, action[1])
            elif action[0] == "attack":
                self._perform_attack(current_player, action[1])

    def _perform_swap(self, current_player, new_creature):
        current_player.active_creature = new_creature
        self._show_text(current_player, f"{current_player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        defender_creature = defender.active_creature
        
        # Calculate damage using floats for intermediate calculations
        if skill.is_physical:
            raw_damage = float(attacker.active_creature.attack) + float(skill.base_damage) - float(defender_creature.defense)
        else:
            raw_damage = (float(attacker.active_creature.sp_attack) / float(defender_creature.sp_defense)) * float(skill.base_damage)

        # Apply type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * float(effectiveness))  # Convert to integer for final damage

        # Apply damage
        defender_creature.hp = max(0, defender_creature.hp - final_damage)

        # Show attack result
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender_creature.display_name} took {final_damage} damage!")

        if defender_creature.hp == 0:
            self._show_text(defender, f"{defender_creature.display_name} was knocked out!")
            self._force_swap(defender)

    def _get_type_effectiveness(self, skill_type, defender_type):
        effectiveness_chart = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness_chart.get((skill_type, defender_type), 1)

    def _force_swap(self, player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if not available_creatures:
            return False

        if len(available_creatures) == 1:
            player.active_creature = available_creatures[0]
        else:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing

        self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        return True

    def _reset_creatures_state(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

    def _check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.player, "Returning to main menu...")
            self._reset_creatures_state()
            self._transition_to_scene("MainMenuScene")
            return True
        elif all(creature.hp == 0 for creature in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.player, "Returning to main menu...")
            self._reset_creatures_state()
            self._transition_to_scene("MainMenuScene")
            return True
        return False
