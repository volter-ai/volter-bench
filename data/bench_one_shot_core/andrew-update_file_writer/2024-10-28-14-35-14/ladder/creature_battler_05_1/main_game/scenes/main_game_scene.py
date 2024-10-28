from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.turn_counter = 0
        self.initialize_battle()

    def initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
Turn: {self.turn_counter}

{self.player.display_name}'s {self.player.active_creature.display_name}
HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp}

{self.opponent.display_name}'s {self.opponent.active_creature.display_name}
HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        while True:
            self.turn_counter += 1
            player_action = self.player_turn(self.player)
            opponent_action = self.player_turn(self.opponent)
            self.resolve_turn(player_action, opponent_action)

            if self.check_battle_end():
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_turn(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if attack_button == choice:
                return self.choose_attack(current_player)
            elif swap_button == choice:
                return self.choose_swap(current_player)

    def choose_attack(self, current_player):
        skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
        back_button = Button("Back")
        choices = skill_choices + [back_button]
        choice = self._wait_for_choice(current_player, choices)

        if choice == back_button:
            return self.player_turn(current_player)
        return ("attack", choice.thing)

    def choose_swap(self, current_player):
        available_creatures = [c for c in current_player.creatures if c != current_player.active_creature and c.hp > 0]
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices = creature_choices + [back_button]
        choice = self._wait_for_choice(current_player, choices)

        if choice == back_button:
            return self.player_turn(current_player)
        return ("swap", choice.thing)

    def resolve_turn(self, player_action, opponent_action):
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]

        # Resolve swaps first
        for player, action in actions:
            if action[0] == "swap":
                self.perform_swap(player, action[1])

        # Resolve attacks
        attack_actions = [(player, action) for player, action in actions if action[0] == "attack"]
        
        # Sort by speed, but randomly shuffle equal speeds
        attack_actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        # Group actions by speed
        speed_groups = {}
        for action in attack_actions:
            speed = action[0].active_creature.speed
            if speed not in speed_groups:
                speed_groups[speed] = []
            speed_groups[speed].append(action)
        
        # Shuffle each speed group and flatten the list
        shuffled_actions = []
        for speed in sorted(speed_groups.keys(), reverse=True):
            group = speed_groups[speed]
            random.shuffle(group)
            shuffled_actions.extend(group)
        
        # Perform attacks in the shuffled order
        for player, action in shuffled_actions:
            self.perform_attack(player, action[1])

    def perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def perform_attack(self, attacker, skill):
        defender = self.opponent if attacker == self.player else self.player
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        else:
            raw_damage = float(attacker.sp_attack) / float(defender.sp_defense) * float(skill.base_damage)

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)

    def get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        for player in [self.player, self.opponent]:
            if all(creature.hp == 0 for creature in player.creatures):
                winner = self.opponent if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins the battle!")
                return True

        if self.player.active_creature.hp == 0:
            self.force_swap(self.player)
        if self.opponent.active_creature.hp == 0:
            self.force_swap(self.opponent)

        return False

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, choices)
            self.perform_swap(player, choice.thing)

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
