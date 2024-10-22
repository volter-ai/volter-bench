from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.turn_counter = 0

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""===Battle===
Turn: {self.turn_counter}

{self.player.display_name}'s {player_creature.display_name}:
HP: {player_creature.hp}/{player_creature.max_hp}

{self.opponent.display_name}'s {opponent_creature.display_name}:
HP: {opponent_creature.hp}/{opponent_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._show_text(self.player, "Battle start!")
        self._show_text(self.opponent, "Battle start!")
        while True:
            self.turn_counter += 1
            player_action = self.player_choice_phase(self.player)
            opponent_action = self.player_choice_phase(self.opponent)
            self.resolution_phase(player_action, opponent_action)

            if self.check_battle_end():
                self.reset_creature_states()
                break

    def player_choice_phase(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if attack_button == choice:
                attack_result = self.choose_attack(current_player)
                if attack_result:
                    return attack_result
            elif swap_button == choice:
                swap_result = self.choose_swap(current_player)
                if swap_result:
                    return swap_result

    def choose_attack(self, current_player):
        back_button = Button("Back")
        choices = [SelectThing(skill, label=skill.display_name) for skill in current_player.active_creature.skills]
        choices.append(back_button)
        choice = self._wait_for_choice(current_player, choices)
        if choice == back_button:
            return None
        return ("attack", choice.thing)

    def choose_swap(self, current_player):
        available_creatures = [c for c in current_player.creatures if c != current_player.active_creature and c.hp > 0]
        if not available_creatures:
            self._show_text(current_player, "No creatures available to swap.")
            return None
        back_button = Button("Back")
        choices = [SelectThing(creature, label=creature.display_name) for creature in available_creatures]
        choices.append(back_button)
        choice = self._wait_for_choice(current_player, choices)
        if choice == back_button:
            return None
        return ("swap", choice.thing)

    def resolution_phase(self, player_action, opponent_action):
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]

        # Sort actions: swaps first, then by speed
        actions.sort(key=lambda x: (x[1][0] != "swap", -x[0].active_creature.speed))

        for current_player, action in actions:
            other_player = self.opponent if current_player == self.player else self.player
            action_type, action_data = action

            if action_type == "swap":
                self.perform_swap(current_player, action_data)
            elif action_type == "attack":
                self.perform_attack(current_player, other_player, action_data)

            if self.check_battle_end():
                return

    def perform_swap(self, player, new_creature):
        old_creature = player.active_creature
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped {old_creature.display_name} for {new_creature.display_name}!")
        self._show_text(self.opponent, f"{player.display_name} swapped {old_creature.display_name} for {new_creature.display_name}!")

    def perform_attack(self, attacker, defender, skill):
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")
        self._show_text(self.opponent, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
            self._show_text(self.opponent, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
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
            return False

        choices = [SelectThing(creature, label=creature.display_name) for creature in available_creatures]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        self._show_text(self.player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        self._show_text(self.opponent, f"{player.display_name} sent out {player.active_creature.display_name}!")
        return True

    def check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creature_states(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
        self._show_text(self.player, "All creatures have been restored to full health.")
        self._show_text(self.opponent, "All creatures have been restored to full health.")
