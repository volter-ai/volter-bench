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
        
        battle_ongoing = True
        while battle_ongoing:
            self.turn_counter += 1
            player_action = self.player_choice_phase(self.player)
            opponent_action = self.player_choice_phase(self.opponent)
            
            if player_action and opponent_action:
                self.resolution_phase(player_action, opponent_action)
            
            battle_result = self.check_battle_end()
            if battle_result is not None:
                battle_ongoing = False
                if battle_result:
                    self._show_text(self.player, "You won the battle!")
                    self._show_text(self.opponent, "You lost the battle!")
                else:
                    self._show_text(self.player, "You lost the battle!")
                    self._show_text(self.opponent, "You won the battle!")

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self, current_player):
        while True:
            attack_button = Button("Attack")
            choices = [attack_button]
            
            if self.has_available_creatures(current_player):
                swap_button = Button("Swap")
                choices.append(swap_button)
            
            choice = self._wait_for_choice(current_player, choices)

            if attack_button == choice:
                action = self.choose_attack(current_player)
            elif swap_button == choice:
                action = self.choose_swap(current_player)
            
            if action:
                return action

    def choose_attack(self, current_player):
        back_button = Button("Back")
        choices = [SelectThing(skill) for skill in current_player.active_creature.skills] + [back_button]
        choice = self._wait_for_choice(current_player, choices)
        if choice == back_button:
            return None
        return choice

    def choose_swap(self, current_player):
        available_creatures = [c for c in current_player.creatures if c.hp > 0 and c != current_player.active_creature]
        if not available_creatures:
            return None
        back_button = Button("Back")
        choices = [SelectThing(creature) for creature in available_creatures] + [back_button]
        choice = self._wait_for_choice(current_player, choices)
        if choice == back_button:
            return None
        return choice

    def has_available_creatures(self, player):
        return any(c.hp > 0 and c != player.active_creature for c in player.creatures)

    def resolution_phase(self, player_action, opponent_action):
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]
        # Sort actions by speed, with a random tiebreaker for equal speeds
        actions.sort(key=lambda x: (x[0].active_creature.speed, random.random()), reverse=True)

        for current_player, action in actions:
            if isinstance(action.thing, Skill):
                self.execute_skill(current_player, action.thing)
            elif isinstance(action.thing, Creature):
                self.swap_creature(current_player, action.thing)

    def execute_skill(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
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

    def swap_creature(self, player, new_creature):
        old_creature = player.active_creature
        player.active_creature = new_creature
        self._show_text(player, f"{old_creature.display_name} was swapped out for {new_creature.display_name}!")
        self._show_text(self.opponent if player == self.player else self.player,
                        f"{player.display_name} swapped {old_creature.display_name} for {new_creature.display_name}!")

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return False

        choices = [SelectThing(creature) for creature in available_creatures]
        new_creature = self._wait_for_choice(player, choices).thing
        self.swap_creature(player, new_creature)
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
            return False  # Player lost
        elif all(c.hp == 0 for c in self.opponent.creatures):
            return True  # Player won
        return None  # Battle is ongoing

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
