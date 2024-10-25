from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


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
3. Return to Main Menu
"""

    def run(self):
        while True:
            self._show_text(self.player, str(self))
            self._show_text(self.opponent, str(self))

            player_action = self.player_choice_phase(self.player)
            if player_action == "return_to_menu":
                self._transition_to_scene("MainMenuScene")
                return

            opponent_action = self.player_choice_phase(self.opponent)

            self.resolution_phase(player_action, opponent_action)

            if self.check_battle_end():
                self._transition_to_scene("MainMenuScene")
                return

    def player_choice_phase(self, current_player):
        choice = self._wait_for_choice(current_player, [
            Button("Attack"),
            Button("Swap"),
            Button("Return to Main Menu")
        ])

        if choice.display_name == "Attack":
            return self.choose_attack(current_player)
        elif choice.display_name == "Swap":
            return self.choose_swap(current_player)
        elif choice.display_name == "Return to Main Menu":
            return "return_to_menu"

    def choose_attack(self, current_player):
        skills = current_player.active_creature.skills
        skill_choices = [SelectThing(skill, label=skill.display_name) for skill in skills]
        skill_choice = self._wait_for_choice(current_player, skill_choices)
        return ("attack", skill_choice.thing)

    def choose_swap(self, current_player):
        available_creatures = [c for c in current_player.creatures if c.hp > 0 and c != current_player.active_creature]
        if not available_creatures:
            self._show_text(current_player, "No available creatures to swap!")
            return self.player_choice_phase(current_player)
        creature_choices = [SelectThing(creature, label=creature.display_name) for creature in available_creatures]
        creature_choice = self._wait_for_choice(current_player, creature_choices)
        return ("swap", creature_choice.thing)

    def resolution_phase(self, player_action, opponent_action):
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]

        # Sort actions: swaps first, then by speed
        actions.sort(key=lambda x: (x[1][0] != "swap", -x[0].active_creature.speed))

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
            "leaf": {"water": 2, "fire": 0.5}
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
