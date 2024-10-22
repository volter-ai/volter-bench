from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


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
        skills = current_player.active_creature.skills
        skill_choices = [SelectThing(skill) for skill in skills]
        back_button = Button("Back")
        choices = skill_choices + [back_button]
        choice = self._wait_for_choice(current_player, choices)

        if choice == back_button:
            return self._player_choice_phase(current_player)
        return ("attack", choice.thing)

    def _choose_swap(self, current_player):
        available_creatures = [c for c in current_player.creatures if c != current_player.active_creature and c.hp > 0]
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
        
        actions.sort(key=lambda x: (x[1][0] != "swap", -x[0].active_creature.speed, random.random()))

        for player, action in actions:
            if action[0] == "swap":
                self._perform_swap(player, action[1])
            elif action[0] == "attack":
                self._perform_attack(player, action[1])

            if self._check_battle_end():
                return

    def _perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(defender, f"{defender.active_creature.display_name} was knocked out!")
            self._force_swap(defender)

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = float(attacker.attack) + float(skill.base_damage) - float(defender.defense)
        else:
            raw_damage = (float(attacker.sp_attack) / float(defender.sp_defense)) * float(skill.base_damage)

        raw_damage = max(1.0, raw_damage)

        type_factor = float(self._get_type_factor(skill.skill_type, defender.creature_type))
        final_damage = int(raw_damage * type_factor)
        return final_damage

    def _get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            self._show_text(player, f"{player.display_name} has no more creatures able to battle!")
            self._end_battle(player)
            return

        if len(available_creatures) == 1:
            player.active_creature = available_creatures[0]
            self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        else:
            self._show_text(player, "Choose a creature to swap to:")
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing
            self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")

    def _end_battle(self, losing_player):
        winning_player = self.bot if losing_player == self.player else self.player
        self._show_text(self.player, f"{winning_player.display_name} won the battle!")
        self._reset_player_creatures()
        self._transition_to_scene("MainMenuScene")

    def _check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._end_battle(self.player)
            return True
        elif all(c.hp == 0 for c in self.bot.creatures):
            self._end_battle(self.bot)
            return True
        return False

    def _reset_player_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
