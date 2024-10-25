from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, RandomModeGracefulExit
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""
Creature Battle!

{self.player.display_name}'s {self.player.active_creature.display_name}:
HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp}

{self.opponent.display_name}'s {self.opponent.active_creature.display_name}:
HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp}

1. Attack
2. Swap
"""

    def run(self):
        try:
            while True:
                self._show_text(self.player, str(self))
                self._show_text(self.opponent, str(self))

                player_action = self.player_choice_phase(self.player)
                opponent_action = self.player_choice_phase(self.opponent)

                self.resolution_phase(player_action, opponent_action)

                if self.check_battle_end():
                    break
        except RandomModeGracefulExit:
            self._show_text(self.player, "Random mode completed. Ending the game.")
            self._show_text(self.opponent, "Random mode completed. Ending the game.")
        finally:
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self, current_player):
        while True:
            main_choice = self._wait_for_choice(current_player, [
                Button("Attack"),
                Button("Swap")
            ])

            if main_choice.display_name == "Attack":
                attack_result = self.choose_attack(current_player)
                if attack_result:
                    return attack_result
            elif main_choice.display_name == "Swap":
                swap_result = self.choose_swap(current_player)
                if swap_result:
                    return swap_result

    def choose_attack(self, current_player):
        skills = current_player.active_creature.skills
        skill_choices = [SelectThing(skill, label=skill.display_name) for skill in skills]
        skill_choices.append(Button("Back"))
        skill_choice = self._wait_for_choice(current_player, skill_choices)
        
        if isinstance(skill_choice, Button) and skill_choice.display_name == "Back":
            return None
        return ("attack", skill_choice.thing)

    def choose_swap(self, current_player):
        available_creatures = [c for c in current_player.creatures if c.hp > 0 and c != current_player.active_creature]
        if not available_creatures:
            self._show_text(current_player, "No creatures available to swap.")
            return None
        
        creature_choices = [SelectThing(creature, label=creature.display_name) for creature in available_creatures]
        creature_choices.append(Button("Back"))
        creature_choice = self._wait_for_choice(current_player, creature_choices)
        
        if isinstance(creature_choice, Button) and creature_choice.display_name == "Back":
            return None
        return ("swap", creature_choice.thing)

    def resolution_phase(self, player_action, opponent_action):
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]

        # Sort actions: swaps first, then by speed, with random tiebreaker for equal speeds
        actions.sort(key=lambda x: (x[1][0] != "swap", -x[0].active_creature.speed, random.random()))

        for current_player, action in actions:
            other_player = self.opponent if current_player == self.player else self.player
            
            if action[0] == "swap":
                current_player.active_creature = action[1]
                self._show_text(self.player, f"{current_player.display_name} swapped to {action[1].display_name}!")
                self._show_text(self.opponent, f"{current_player.display_name} swapped to {action[1].display_name}!")
            elif action[0] == "attack":
                self.execute_attack(current_player, other_player, action[1])

            if self.check_battle_end():
                return

    def execute_attack(self, attacker, defender, skill):
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)

        self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")
        self._show_text(self.opponent, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

        if defender.active_creature.hp == 0:
            self.force_swap(defender)

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5},
            "normal": {}  # Normal type is neither effective nor ineffective against any type
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return

        creature_choices = [SelectThing(creature, label=creature.display_name) for creature in available_creatures]
        new_creature = self._wait_for_choice(player, creature_choices).thing
        player.active_creature = new_creature

        self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")
        self._show_text(self.opponent, f"{player.display_name} swapped to {new_creature.display_name}!")

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
