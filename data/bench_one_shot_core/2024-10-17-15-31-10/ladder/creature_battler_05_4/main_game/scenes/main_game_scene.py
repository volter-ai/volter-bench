import random
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.turn_counter = 0

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""===Battle===
Turn: {self.turn_counter}

{self.player.display_name}'s {player_creature.display_name}:
HP: {player_creature.hp}/{player_creature.max_hp}

{self.opponent.display_name}'s {opponent_creature.display_name}:
HP: {opponent_creature.hp}/{opponent_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._show_text(self.player, "Battle start!")
        self._show_text(self.opponent, "Battle start!")
        
        while True:
            self.turn_counter += 1
            player_action = self.player_choice_phase(self.player)
            if player_action is None:
                self._show_text(self.player, f"{self.player.display_name} has no more creatures able to battle!")
                self._show_text(self.opponent, f"{self.player.display_name} has no more creatures able to battle!")
                self._show_text(self.player, f"{self.opponent.display_name} wins the battle!")
                self._show_text(self.opponent, f"{self.opponent.display_name} wins the battle!")
                break
            
            opponent_action = self.player_choice_phase(self.opponent)
            if opponent_action is None:
                self._show_text(self.player, f"{self.opponent.display_name} has no more creatures able to battle!")
                self._show_text(self.opponent, f"{self.opponent.display_name} has no more creatures able to battle!")
                self._show_text(self.player, f"{self.player.display_name} wins the battle!")
                self._show_text(self.opponent, f"{self.player.display_name} wins the battle!")
                break
            
            self.resolution_phase(player_action, opponent_action)

        self.reset_creatures()

    def player_choice_phase(self, current_player):
        can_swap = self.has_available_creatures(current_player)
        
        while True:
            main_choices = [Button("Attack")]
            if can_swap:
                main_choices.append(Button("Swap"))
            
            if not main_choices:
                return None  # No available actions
            
            main_choice = self._wait_for_choice(current_player, main_choices)

            if main_choice.display_name == "Attack":
                attack_result = self.choose_attack(current_player)
                if attack_result:
                    return attack_result
            elif main_choice.display_name == "Swap":
                swap_result = self.choose_swap(current_player)
                if swap_result:
                    return swap_result

    def choose_attack(self, current_player):
        skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
        skill_choices.append(Button("Back"))
        skill_choice = self._wait_for_choice(current_player, skill_choices)
        
        if isinstance(skill_choice, Button) and skill_choice.display_name == "Back":
            return None
        return ("attack", skill_choice.thing)

    def choose_swap(self, current_player):
        available_creatures = [creature for creature in current_player.creatures if creature.hp > 0 and creature != current_player.active_creature]
        if not available_creatures:
            return None
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        creature_choices.append(Button("Back"))
        creature_choice = self._wait_for_choice(current_player, creature_choices)
        
        if isinstance(creature_choice, Button) and creature_choice.display_name == "Back":
            return None
        return ("swap", creature_choice.thing)

    def has_available_creatures(self, player):
        return any(creature.hp > 0 for creature in player.creatures if creature != player.active_creature)

    def resolution_phase(self, player_action, opponent_action):
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]
        
        sorted_actions = self.sort_actions_by_speed(actions)

        for current_player, action in sorted_actions:
            other_player = self.opponent if current_player == self.player else self.player
            
            if action[0] == "swap":
                self.perform_swap(current_player, action[1])
            elif action[0] == "attack":
                self.perform_attack(current_player, other_player, action[1])

    def sort_actions_by_speed(self, actions):
        def speed_key(action):
            player, (action_type, _) = action
            if action_type == "swap":
                return float('inf')  # Swaps always go first
            return player.active_creature.speed

        # Sort actions based on speed (higher speed goes first)
        sorted_actions = sorted(actions, key=speed_key, reverse=True)

        # Handle speed ties
        if len(sorted_actions) == 2:
            player1, action1 = sorted_actions[0]
            player2, action2 = sorted_actions[1]
            if speed_key((player1, action1)) == speed_key((player2, action2)):
                # Randomly choose the order for speed ties
                return random.sample(sorted_actions, len(sorted_actions))

        return sorted_actions

    def perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")
        self._show_text(self.opponent, f"{player.display_name} swapped to {new_creature.display_name}!")

    def perform_attack(self, attacker, defender, skill):
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.opponent, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} took {damage} damage!")
        self._show_text(self.opponent, f"{defender.display_name}'s {defender.active_creature.display_name} took {damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
            self._show_text(self.opponent, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
            self.force_swap(defender)

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_effectiveness(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def force_swap(self, player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if not available_creatures:
            return

        creature_choices = [SelectThing(creature) for creature in available_creatures]
        new_creature = self._wait_for_choice(player, creature_choices).thing
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} sent out {new_creature.display_name}!")
        self._show_text(self.opponent, f"{player.display_name} sent out {new_creature.display_name}!")

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
