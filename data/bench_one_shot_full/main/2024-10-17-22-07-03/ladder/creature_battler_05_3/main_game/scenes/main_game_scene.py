from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
{self.opponent.display_name}: {self.opponent.active_creature.display_name} (HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp})

> Attack
> Swap
"""

    def run(self):
        while True:
            player_action = self.player_turn()
            opponent_action = self.opponent_turn()
            
            self.resolve_actions(player_action, opponent_action)
            
            if self.check_battle_end():
                self.reset_creatures_state()
                break

    def player_turn(self):
        self._show_text(self.player, f"It's your turn, {self.player.display_name}!")
        return self.get_player_action(self.player)

    def opponent_turn(self):
        self._show_text(self.player, f"It's {self.opponent.display_name}'s turn!")
        return self.get_player_action(self.opponent)

    def get_player_action(self, acting_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(acting_player, choices)

            if attack_button == choice:
                action = self.get_attack_action(acting_player)
                if action:
                    return action
            elif swap_button == choice:
                action = self.get_swap_action(acting_player)
                if action:
                    return action

    def get_attack_action(self, acting_player):
        skill_choices = [SelectThing(skill, label=skill.display_name) for skill in acting_player.active_creature.skills]
        back_button = Button("Back")
        choices = skill_choices + [back_button]
        choice = self._wait_for_choice(acting_player, choices)
        
        if choice == back_button:
            return None
        return choice

    def get_swap_action(self, acting_player):
        available_creatures = [c for c in acting_player.creatures if c != acting_player.active_creature and c.hp > 0]
        if not available_creatures:
            self._show_text(acting_player, "No creatures available to swap.")
            return None
        
        creature_choices = [SelectThing(creature, label=creature.display_name) for creature in available_creatures]
        back_button = Button("Back")
        choices = creature_choices + [back_button]
        choice = self._wait_for_choice(acting_player, choices)
        
        if choice == back_button:
            return None
        return choice

    def resolve_actions(self, player_action, opponent_action):
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]
        
        # Prioritize swap actions
        swap_actions = [action for action in actions if isinstance(action[1].thing, Creature)]
        for player, action in swap_actions:
            self.execute_swap(player, action.thing)
        
        # Execute skill actions based on speed, with random resolution for ties
        skill_actions = [action for action in actions if isinstance(action[1].thing, Skill)]
        sorted_skill_actions = self.sort_actions_by_speed(skill_actions)
        
        for player, action in sorted_skill_actions:
            opponent = self.opponent if player == self.player else self.player
            self.execute_attack(player, opponent, action.thing)
            if self.check_knockout(opponent):
                if not self.force_swap(opponent):
                    break

    def sort_actions_by_speed(self, actions):
        # Group actions by speed
        speed_groups = {}
        for action in actions:
            speed = action[0].active_creature.speed
            if speed not in speed_groups:
                speed_groups[speed] = []
            speed_groups[speed].append(action)
        
        # Shuffle actions within each speed group
        for speed in speed_groups:
            random.shuffle(speed_groups[speed])
        
        # Sort speed groups and flatten the list
        sorted_actions = []
        for speed in sorted(speed_groups.keys(), reverse=True):
            sorted_actions.extend(speed_groups[speed])
        
        return sorted_actions

    def execute_attack(self, attacker, defender, skill):
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender.active_creature.display_name}!")

    def execute_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")

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

    def check_knockout(self, player):
        return player.active_creature.hp == 0

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return False
        
        if player == self.player:
            self._show_text(player, f"{player.active_creature.display_name} was knocked out! Choose a new creature.")
            swap_action = self.get_swap_action(player)
            if swap_action:
                self.execute_swap(player, swap_action.thing)
                return True
        else:
            new_creature = random.choice(available_creatures)
            self.execute_swap(player, new_creature)
            return True
        
        return False

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, f"{self.opponent.display_name} wins!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif all(creature.hp == 0 for creature in self.opponent.creatures):
            self._show_text(self.player, f"{self.player.display_name} wins!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creatures_state(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
