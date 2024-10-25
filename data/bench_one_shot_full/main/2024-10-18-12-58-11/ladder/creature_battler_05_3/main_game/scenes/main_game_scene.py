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
        skill_choices = [SelectThing(skill, label=skill.display_name) for skill in acting_player.active_creature.skills]
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
        creature_choices = [SelectThing(creature, label=creature.display_name) for creature in available_creatures]
        back_button = Button("Back")
        creature_choices.append(back_button)
        choice = self._wait_for_choice(acting_player, creature_choices)
        if choice == back_button:
            return None
        return choice

    def resolve_actions(self, player_action, opponent_action):
        actions = [(self.player, player_action), (self.opponent, opponent_action)]
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        if actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
            random.shuffle(actions)

        for acting_player, action in actions:
            defending_player = self.opponent if acting_player == self.player else self.player
            self.execute_action(acting_player, defending_player, action)
            if self.check_knockout(defending_player):
                if not self.force_swap(defending_player):
                    return

    def execute_action(self, acting_player, defending_player, action):
        if isinstance(action.thing, Skill):
            self.execute_attack(acting_player, defending_player, action.thing)
        elif isinstance(action.thing, Creature):
            self.execute_swap(acting_player, action.thing)

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
        new_creature = random.choice(available_creatures)
        self.execute_swap(player, new_creature)
        return True

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
