from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, RandomModeGracefulExit
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]
        self.game_over = False

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
            while not self.game_over:
                self._show_text(self.player, str(self))
                self._show_text(self.opponent, str(self))

                player_action = self.player_choice_phase(self.player)
                opponent_action = self.player_choice_phase(self.opponent)

                if player_action is None or opponent_action is None:
                    break

                self.resolution_phase(player_action, opponent_action)

                if self.check_battle_end():
                    self.game_over = True

            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
        except RandomModeGracefulExit:
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self, current_player):
        while True:
            try:
                choice = self._wait_for_choice(current_player, [
                    Button("Attack"),
                    Button("Swap"),
                    Button("Back")
                ])

                if choice.display_name == "Attack":
                    attack_action = self.choose_attack(current_player)
                    if attack_action:
                        return attack_action
                elif choice.display_name == "Swap":
                    swap_action = self.choose_swap(current_player)
                    if swap_action:
                        return swap_action
                elif choice.display_name == "Back":
                    return None
            except RandomModeGracefulExit:
                return None

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
            self._show_text(current_player, f"{current_player.display_name} has no available creatures to swap!")
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

        # Sort actions: swaps first, then by speed (with random tiebreaker)
        actions.sort(key=lambda x: (
            x[1][0] != "swap",
            -x[0].active_creature.speed,
            random.random()
        ))

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
            raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        else:
            raw_damage = float(attacker.sp_attack) / float(defender.sp_defense) * float(skill.base_damage)

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

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
