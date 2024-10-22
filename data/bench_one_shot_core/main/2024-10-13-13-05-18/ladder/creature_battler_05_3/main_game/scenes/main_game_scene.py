from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]
        self.action_queue = []

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
{self.opponent.display_name}: {self.opponent.active_creature.display_name} (HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp})

> Attack
> Swap
"""

    def run(self):
        while True:
            self.action_queue = []
            self.player_turn()
            if self.check_battle_end():
                break
            self.opponent_turn()
            if self.check_battle_end():
                break
            self.resolution_phase()
            if self.check_battle_end():
                break
        self.reset_creatures_state()
        self._quit_whole_game()

    def player_turn(self):
        self._show_text(self.player, f"It's your turn, {self.player.display_name}!")
        action = self.get_player_action(self.player)
        if action:
            self.action_queue.append((self.player, action))

    def opponent_turn(self):
        self._show_text(self.player, f"It's {self.opponent.display_name}'s turn!")
        action = self.get_player_action(self.opponent)
        if action:
            self.action_queue.append((self.opponent, action))

    def get_player_action(self, acting_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            back_button = Button("Back")
            choices = [attack_button, swap_button, back_button]
            choice = self._wait_for_choice(acting_player, choices)

            if attack_button == choice:
                action = self.get_attack_action(acting_player)
                if action:
                    return action
            elif swap_button == choice:
                action = self.get_swap_action(acting_player)
                if action:
                    return action
            elif back_button == choice:
                continue

    def get_attack_action(self, acting_player):
        skill_choices = [SelectThing(skill) for skill in acting_player.active_creature.skills]
        back_button = Button("Back")
        skill_choices.append(back_button)
        choice = self._wait_for_choice(acting_player, skill_choices)
        if choice == back_button:
            return None
        return choice

    def get_swap_action(self, acting_player):
        available_creatures = [c for c in acting_player.creatures if c != acting_player.active_creature and c.hp > 0]
        if not available_creatures:
            self._show_text(acting_player, "No creatures available to swap!")
            return None
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        creature_choices.append(back_button)
        choice = self._wait_for_choice(acting_player, creature_choices)
        if choice == back_button:
            return None
        return choice

    def resolution_phase(self):
        # Sort action queue based on speed and randomize for same speed
        self.action_queue.sort(key=lambda x: (-x[0].active_creature.speed, random.random()))

        for player, action in self.action_queue:
            if isinstance(action.thing, Skill):
                self.execute_attack(player, self.get_opponent(player), action.thing)
            elif isinstance(action.thing, Creature):
                self.execute_swap(player, action.thing)
                # Hit swapped-in creature with queued skill
                opponent = self.get_opponent(player)
                opponent_action = next((a for p, a in self.action_queue if p == opponent), None)
                if opponent_action and isinstance(opponent_action.thing, Skill):
                    self.execute_attack(opponent, player, opponent_action.thing)

    def get_opponent(self, player):
        return self.opponent if player == self.player else self.player

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

        type_factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
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

    def check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, f"All your creatures have fainted. {self.opponent.display_name} wins!")
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, f"All opponent's creatures have fainted. You win!")
            return True
        elif self.player.active_creature.hp == 0:
            return not self.force_swap(self.player)
        elif self.opponent.active_creature.hp == 0:
            return not self.force_swap(self.opponent)
        return False

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            new_creature = self._wait_for_choice(player, creature_choices).thing
            player.active_creature = new_creature
            self._show_text(self.player, f"{player.display_name} was forced to swap to {new_creature.display_name}!")
            return True
        else:
            self._show_text(self.player, f"{player.display_name} has no more creatures available!")
            return False

    def reset_creatures_state(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
