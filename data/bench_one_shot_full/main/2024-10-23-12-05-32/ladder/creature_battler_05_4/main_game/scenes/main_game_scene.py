from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.turn_counter = 0

    def __str__(self):
        return f"""===Battle===
Turn: {self.turn_counter}

{self.player.display_name}:
Active Creature: {self.player.active_creature.display_name}
HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp}

{self.opponent.display_name}:
Active Creature: {self.opponent.active_creature.display_name}
HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent.display_name} appeared!")
        while True:
            self.turn_counter += 1
            player_action = self.player_turn()
            opponent_action = self.opponent_turn()
            self.resolve_turn(player_action, opponent_action)
            
            if self.check_battle_end():
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if attack_button == choice:
                action = self.choose_attack(self.player)
            elif swap_button == choice:
                action = self.choose_swap(self.player)
            
            if action:
                return action

    def opponent_turn(self):
        swap_action = self.choose_swap(self.opponent)
        if swap_action:
            return swap_action
        return self.choose_attack(self.opponent)

    def choose_attack(self, player: Player):
        back_button = Button("Back")
        choices = [SelectThing(skill) for skill in player.active_creature.skills] + [back_button]
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return None
        return choice

    def choose_swap(self, player: Player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        if not available_creatures:
            return None
        back_button = Button("Back")
        choices = [SelectThing(creature) for creature in available_creatures] + [back_button]
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return None
        return choice

    def resolve_turn(self, player_action, opponent_action):
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]
        # Sort by speed, with random tiebreaker
        actions.sort(key=lambda x: (x[0].active_creature.speed, random.random()), reverse=True)

        for player, action in actions:
            if action is None:
                continue
            if isinstance(action.thing, Creature):
                self.swap_creature(player, action.thing)
            elif isinstance(action.thing, Skill):
                self.use_skill(player, action.thing)

    def swap_creature(self, player: Player, new_creature: Creature):
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def use_skill(self, attacker: Player, skill: Skill):
        defender = self.opponent if attacker == self.player else self.player
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender.active_creature.display_name}!")

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_factor)

    def get_type_effectiveness(self, skill_type: str, defender_type: str):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
