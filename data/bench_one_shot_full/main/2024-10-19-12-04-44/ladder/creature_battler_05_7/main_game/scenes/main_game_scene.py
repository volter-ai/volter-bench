import random
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill


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
            opponent_action = self.player_choice_phase(self.opponent)
            self.resolution_phase(player_action, opponent_action)

            if self.check_battle_end():
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

    def player_choice_phase(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if attack_button == choice:
                action = self.choose_attack(current_player)
            elif swap_button == choice:
                action = self.choose_swap(current_player)
            
            if action is not None:
                return action

    def choose_attack(self, current_player):
        choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(current_player, choices)
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return choice

    def choose_swap(self, current_player):
        available_creatures = [c for c in current_player.creatures if c.hp > 0 and c != current_player.active_creature]
        if not available_creatures:
            self._show_text(current_player, "No creatures available to swap!")
            return None
        choices = [SelectThing(creature) for creature in available_creatures]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(current_player, choices)
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return choice

    def resolution_phase(self, player_action, opponent_action):
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]
        
        # Prioritize swaps
        swap_actions = [action for action in actions if isinstance(action[1].thing, Creature)]
        attack_actions = [action for action in actions if isinstance(action[1].thing, Skill)]
        
        # Execute swaps first
        for current_player, action in swap_actions:
            self.swap_creature(current_player, action.thing)
        
        # Then execute attacks
        if attack_actions:
            # Sort by speed, with random tiebreaker
            attack_actions.sort(key=lambda x: (x[0].active_creature.speed, random.random()), reverse=True)
            for current_player, action in attack_actions:
                self.execute_skill(current_player, action.thing)

    def execute_skill(self, attacker, skill):
        defender = self.opponent if attacker == self.player else self.player
        defender_creature = defender.active_creature

        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        type_factor = self.get_type_effectiveness(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * type_factor)

        defender_creature.hp = max(0, defender_creature.hp - final_damage)

        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{attacker.active_creature.display_name} used {skill.display_name}!")

        if type_factor > 1:
            self._show_text(attacker, "It's super effective!")
            self._show_text(defender, "It's super effective!")
        elif type_factor < 1:
            self._show_text(attacker, "It's not very effective...")
            self._show_text(defender, "It's not very effective...")

        self._show_text(attacker, f"{defender_creature.display_name} took {final_damage} damage!")
        self._show_text(defender, f"{defender_creature.display_name} took {final_damage} damage!")

        if defender_creature.hp == 0:
            self._show_text(attacker, f"{defender_creature.display_name} fainted!")
            self._show_text(defender, f"{defender_creature.display_name} fainted!")
            self.force_swap(defender)

    def swap_creature(self, current_player, new_creature):
        old_creature = current_player.active_creature
        current_player.active_creature = new_creature
        self._show_text(current_player, f"{old_creature.display_name} was swapped out for {new_creature.display_name}!")
        self._show_text(self.opponent if current_player == self.player else self.player,
                        f"{current_player.display_name} swapped {old_creature.display_name} for {new_creature.display_name}!")

    def force_swap(self, current_player):
        available_creatures = [c for c in current_player.creatures if c.hp > 0]
        if not available_creatures:
            return False

        choices = [SelectThing(creature) for creature in available_creatures]
        new_creature = self._wait_for_choice(current_player, choices).thing
        self.swap_creature(current_player, new_creature)
        return True

    def get_type_effectiveness(self, skill_type, creature_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)

    def check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            return True
        return False

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
