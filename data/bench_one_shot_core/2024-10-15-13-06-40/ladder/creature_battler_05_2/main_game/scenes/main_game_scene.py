from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.turn_counter = 0
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
Turn: {self.turn_counter}

{self.player.display_name}'s {self.player.active_creature.display_name}
HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp}

{self.opponent.display_name}'s {self.opponent.active_creature.display_name}
HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        while True:
            self.turn_counter += 1
            
            if self.check_battle_end():
                break

            player_action = self.player_turn(self.player)
            opponent_action = self.player_turn(self.opponent)
            self.resolve_turn(player_action, opponent_action)

        self.reset_creatures_state()
        self._transition_to_scene("MainMenuScene")

    def player_turn(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if choice == attack_button:
                action = self.choose_attack(current_player)
            elif choice == swap_button:
                action = self.choose_swap(current_player)
            
            if action is not None:
                return action

    def choose_attack(self, current_player):
        skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
        back_button = Button("Back")
        skill_choices.append(back_button)
        choice = self._wait_for_choice(current_player, skill_choices)
        
        if choice == back_button:
            return None
        return ("attack", choice.thing)

    def choose_swap(self, current_player):
        available_creatures = [creature for creature in current_player.creatures if creature.hp > 0 and creature != current_player.active_creature]
        if not available_creatures:
            self._show_text(current_player, f"No creatures available to swap.")
            return None
        
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        creature_choices.append(back_button)
        choice = self._wait_for_choice(current_player, creature_choices)
        
        if choice == back_button:
            return None
        return ("swap", choice.thing)

    def resolve_turn(self, player_action, opponent_action):
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]
        
        # Sort by speed, with random order for equal speeds
        actions.sort(key=lambda x: (x[0].active_creature.speed, random.random()), reverse=True)

        for current_player, action in actions:
            other_player = self.opponent if current_player == self.player else self.player
            action_type, action_target = action

            if action_type == "swap":
                current_player.active_creature = action_target
                self._show_text(current_player, f"{current_player.display_name} swapped to {action_target.display_name}!")
            elif action_type == "attack":
                damage = self.calculate_damage(current_player.active_creature, other_player.active_creature, action_target)
                other_player.active_creature.hp = max(0, other_player.active_creature.hp - damage)
                self._show_text(current_player, f"{current_player.active_creature.display_name} used {action_target.display_name} and dealt {damage} damage!")

            if other_player.active_creature.hp == 0:
                self.handle_fainted_creature(other_player)

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        return max(1, final_damage)

    def get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def handle_fainted_creature(self, player):
        self._show_text(player, f"{player.active_creature.display_name} fainted!")
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if available_creatures:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            new_creature = self._wait_for_choice(player, creature_choices).thing
            player.active_creature = new_creature
            self._show_text(player, f"{player.display_name} sent out {new_creature.display_name}!")
        else:
            self._show_text(player, f"{player.display_name} has no more creatures able to battle!")

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
