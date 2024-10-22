from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
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
                break
        self.reset_creatures_state()

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
                action = self.get_attack_choice(acting_player)
            elif swap_button == choice:
                action = self.get_swap_choice(acting_player)
            
            if action:
                return action
            else:
                self._show_text(acting_player, "Invalid choice. Please try again.")

    def get_attack_choice(self, acting_player):
        back_button = Button("Back")
        choices = [SelectThing(skill) for skill in acting_player.active_creature.skills] + [back_button]
        choice = self._wait_for_choice(acting_player, choices)
        if choice == back_button:
            return None
        return choice

    def get_swap_choice(self, acting_player):
        back_button = Button("Back")
        available_creatures = [c for c in acting_player.creatures if c != acting_player.active_creature and c.hp > 0]
        if not available_creatures:
            self._show_text(acting_player, "No creatures available to swap!")
            return None
        choices = [SelectThing(creature) for creature in available_creatures] + [back_button]
        choice = self._wait_for_choice(acting_player, choices)
        if choice == back_button:
            return None
        return choice

    def resolve_actions(self, player_action, opponent_action):
        actions = [(self.player, player_action), (self.opponent, opponent_action)]
        
        # Sort actions based on speed and randomize ties
        actions.sort(key=lambda x: (x[0].active_creature.speed, random.random()), reverse=True)

        for acting_player, action in actions:
            if isinstance(action.thing, Skill):
                defending_player = self.opponent if acting_player == self.player else self.player
                self.execute_attack(acting_player, defending_player, action.thing)
            elif isinstance(action.thing, Creature):
                self.execute_swap(acting_player, action.thing)

            if self.check_battle_end():
                break

    def execute_attack(self, attacker, defender, skill):
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender.active_creature.display_name}!")
        
        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} fainted!")
            self.force_swap(defender)

    def execute_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_effectiveness(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("water", "fire"): 2,
            ("leaf", "water"): 2,
            ("fire", "water"): 0.5,
            ("water", "leaf"): 0.5,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, f"All your creatures have fainted. {self.opponent.display_name} wins!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif all(creature.hp == 0 for creature in self.opponent.creatures):
            self._show_text(self.player, f"All opponent's creatures have fainted. You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return False
        choices = [SelectThing(creature) for creature in available_creatures]
        new_creature = self._wait_for_choice(player, choices).thing
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} sent out {new_creature.display_name}!")
        return True

    def reset_creatures_state(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
