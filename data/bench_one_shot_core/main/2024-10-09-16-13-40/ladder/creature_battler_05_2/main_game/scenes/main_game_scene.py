from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.turn_counter = 0

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        return f"""===Battle===
Turn: {self.turn_counter}

{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.bot.display_name}'s {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

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

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def _player_choice_phase(self, current_player):
        if current_player.active_creature.hp == 0:
            return self._forced_swap(current_player)

        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choices = [attack_button, swap_button]
        choice = self._wait_for_choice(current_player, choices)

        if choice == attack_button:
            return self._choose_attack(current_player)
        elif choice == swap_button:
            return self._choose_swap(current_player)

    def _forced_swap(self, current_player):
        available_creatures = [creature for creature in current_player.creatures if creature.hp > 0]
        if not available_creatures:
            return None  # No available creatures, battle will end

        creature_choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(current_player, creature_choices)
        return ("swap", choice.thing)

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
        
        # Handle swaps first
        for current_player, action in actions:
            if action and action[0] == "swap":
                self._perform_swap(current_player, action[1])

        # Then handle attacks based on speed
        attack_actions = [(player, action) for player, action in actions if action and action[0] == "attack"]
        if len(attack_actions) == 2:
            player1, action1 = attack_actions[0]
            player2, action2 = attack_actions[1]
            speed1 = player1.active_creature.speed
            speed2 = player2.active_creature.speed

            if speed1 > speed2 or (speed1 == speed2 and random.random() < 0.5):
                self._perform_attack(player1, action1[1], player2.active_creature)
                if player2.active_creature.hp > 0:
                    self._perform_attack(player2, action2[1], player1.active_creature)
            else:
                self._perform_attack(player2, action2[1], player1.active_creature)
                if player1.active_creature.hp > 0:
                    self._perform_attack(player1, action1[1], player2.active_creature)
        elif len(attack_actions) == 1:
            player, action = attack_actions[0]
            opponent = self.bot if player == self.player else self.player
            self._perform_attack(player, action[1], opponent.active_creature)

    def _perform_swap(self, current_player, new_creature):
        current_player.active_creature = new_creature
        self._show_text(current_player, f"{current_player.display_name} swapped to {new_creature.display_name}!")

    def _perform_attack(self, attacker, skill, target):
        damage = self._calculate_damage(attacker.active_creature, target, skill)
        target.hp = max(0, target.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage to {target.display_name}!")

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
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _check_battle_end(self):
        for current_player in [self.player, self.bot]:
            if all(creature.hp == 0 for creature in current_player.creatures):
                winner = self.bot if current_player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins the battle!")
                return True
        return False

    def _reset_creatures(self):
        for player in [self.player, self.bot]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
