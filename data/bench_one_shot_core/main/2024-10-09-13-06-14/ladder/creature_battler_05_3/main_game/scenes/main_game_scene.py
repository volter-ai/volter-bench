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
            battle_ended, winner = self.check_battle_end()
            if battle_ended:
                self._show_text(self.player, f"{'You won' if winner == self.player else 'You lost'} the battle!")
                self.reset_creatures()
                self._quit_whole_game()
                return

            player_action = self.get_player_action(self.player)
            opponent_action = self.get_player_action(self.opponent)

            self.resolve_turn(player_action, opponent_action)

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if choice == attack_button:
                action = self.get_attack_action(player)
            elif choice == swap_button:
                action = self.get_swap_action(player)

            if action is not None:
                return action

    def get_attack_action(self, player):
        back_button = Button("Back")
        choices = [SelectThing(skill) for skill in player.active_creature.skills] + [back_button]
        choice = self._wait_for_choice(player, choices)
        return choice if choice != back_button else None

    def get_swap_action(self, player):
        back_button = Button("Back")
        choices = [SelectThing(creature) for creature in player.creatures if creature != player.active_creature and creature.hp > 0] + [back_button]
        if not choices:
            self._show_text(player, f"{player.display_name} has no creatures to swap to!")
            return None
        choice = self._wait_for_choice(player, choices)
        return choice if choice != back_button else None

    def resolve_turn(self, player_action, opponent_action):
        actions = [(self.player, player_action), (self.opponent, opponent_action)]
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        if actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
            random.shuffle(actions)

        for player, action in actions:
            if isinstance(action.thing, Skill):
                self.resolve_attack(player, action.thing)
            elif isinstance(action.thing, Creature):
                self.swap_creature(player, action.thing)

            if self.check_knocked_out():
                break

    def resolve_attack(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")

    def swap_creature(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(player, f"Swapped to {new_creature.display_name}!")

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        return max(1, final_damage)

    def get_type_effectiveness(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            return True, self.opponent
        elif all(creature.hp == 0 for creature in self.opponent.creatures):
            return True, self.player
        return False, None

    def check_knocked_out(self):
        for player in [self.player, self.opponent]:
            if player.active_creature.hp == 0:
                available_creatures = [c for c in player.creatures if c.hp > 0]
                if available_creatures:
                    new_creature = self.force_swap(player, available_creatures)
                    self.swap_creature(player, new_creature)
                else:
                    return True
        return False

    def force_swap(self, player, available_creatures):
        choices = [SelectThing(creature) for creature in available_creatures]
        self._show_text(player, f"{player.active_creature.display_name} was knocked out! Choose a new creature:")
        return self._wait_for_choice(player, choices).thing

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
