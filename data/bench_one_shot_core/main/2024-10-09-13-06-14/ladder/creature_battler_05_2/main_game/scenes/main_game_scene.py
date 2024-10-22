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
            if self.check_battle_end():
                self.reset_creatures_state()
                self._quit_whole_game()
                return

            player_action = self.player_turn(self.player)
            opponent_action = self.player_turn(self.opponent)

            self.resolve_turn(player_action, opponent_action)

            if self.check_battle_end():
                self.reset_creatures_state()
                self._quit_whole_game()
                return

    def player_turn(self, current_player):
        while True:
            action = self.get_player_action(current_player)
            if action:
                return action

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")
        choices = [attack_button, swap_button]
        choice = self._wait_for_choice(player, choices)

        if choice == attack_button:
            return self.get_attack_choice(player)
        elif choice == swap_button:
            return self.get_swap_choice(player)

    def get_attack_choice(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return choice

    def get_swap_choice(self, player):
        choices = [SelectThing(creature) for creature in player.creatures if creature != player.active_creature and creature.hp > 0]
        choices.append(Button("Back"))
        if not choices:
            self._show_text(player, f"No creatures available to swap!")
            return None
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return choice

    def resolve_turn(self, player_action, opponent_action):
        actions = [(self.player, player_action), (self.opponent, opponent_action)]
        # Sort actions based on speed and a small random factor
        actions.sort(key=lambda x: (x[0].active_creature.speed + random.random(), random.random()), reverse=True)

        for actor, action in actions:
            if isinstance(action.thing, Skill):
                self.resolve_attack(actor, self.get_opponent(actor), action.thing)
            elif isinstance(action.thing, Creature):
                self.swap_creature(actor, action.thing)

            if self.check_forced_swap(actor):
                self.forced_swap(actor)

    def resolve_attack(self, attacker, defender, skill):
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

    def check_forced_swap(self, player):
        return player.active_creature.hp == 0

    def forced_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if available_creatures:
            new_creature = random.choice(available_creatures)
            self.swap_creature(player, new_creature)
        else:
            self._show_text(player, f"{player.display_name} has no more creatures to swap!")

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures_state(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp

    def get_opponent(self, player):
        return self.opponent if player == self.player else self.player
