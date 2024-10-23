from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.turn_counter = 0
        self.battle_result = None

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
        self.game_loop()

    def game_loop(self):
        while True:
            self.turn_counter += 1
            
            if not self.check_battle_continue():
                break

            player_action = self.player_choice_phase(self.player)
            opponent_action = self.player_choice_phase(self.opponent)
            self.resolution_phase(player_action, opponent_action)

            if self.check_battle_end():
                break

        self.end_battle()

    def check_battle_continue(self):
        player_can_continue = any(creature.hp > 0 for creature in self.player.creatures)
        opponent_can_continue = any(creature.hp > 0 for creature in self.opponent.creatures)
        return player_can_continue and opponent_can_continue

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
        skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
        choices = skill_choices + [back_button]
        skill_choice = self._wait_for_choice(current_player, choices)
        
        if skill_choice == back_button:
            return None
        return ("attack", skill_choice.thing)

    def choose_swap(self, current_player):
        available_creatures = [creature for creature in current_player.creatures if creature.hp > 0 and creature != current_player.active_creature]
        if not available_creatures:
            return None
        
        back_button = Button("Back")
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        choices = creature_choices + [back_button]
        creature_choice = self._wait_for_choice(current_player, choices)
        
        if creature_choice == back_button:
            return None
        return ("swap", creature_choice.thing)

    def resolution_phase(self, player_action, opponent_action):
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)

        for current_player, action in actions:
            other_player = self.opponent if current_player == self.player else self.player
            action_type, action_target = action

            if action_type == "swap":
                current_player.active_creature = action_target
                self._show_text(self.player, f"{current_player.display_name} swapped to {action_target.display_name}!")
                self._show_text(self.opponent, f"{current_player.display_name} swapped to {action_target.display_name}!")
            elif action_type == "attack":
                self.execute_attack(current_player, other_player, action_target)

            if self.check_battle_end():
                return

    def execute_attack(self, attacker, defender, skill):
        attacker_creature = attacker.active_creature
        defender_creature = defender.active_creature

        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * type_factor)

        defender_creature.hp = max(0, defender_creature.hp - final_damage)

        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name} on {defender_creature.display_name}!")
        self._show_text(self.opponent, f"{attacker_creature.display_name} used {skill.display_name} on {defender_creature.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {final_damage} damage!")
        self._show_text(self.opponent, f"{defender_creature.display_name} took {final_damage} damage!")

        if defender_creature.hp == 0:
            self._show_text(self.player, f"{defender_creature.display_name} fainted!")
            self._show_text(self.opponent, f"{defender_creature.display_name} fainted!")
            self.force_swap(defender)

    def get_type_factor(self, skill_type, creature_type):
        type_chart = {
            "normal": {"normal": 1, "fire": 1, "water": 1, "leaf": 1},
            "fire": {"normal": 1, "fire": 1, "water": 0.5, "leaf": 2},
            "water": {"normal": 1, "fire": 2, "water": 1, "leaf": 0.5},
            "leaf": {"normal": 1, "fire": 0.5, "water": 2, "leaf": 1}
        }
        return type_chart[skill_type][creature_type]

    def force_swap(self, player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if not available_creatures:
            return

        creature_choices = [SelectThing(creature) for creature in available_creatures]
        creature_choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = creature_choice.thing

        self._show_text(self.player, f"{player.display_name} swapped to {player.active_creature.display_name}!")
        self._show_text(self.opponent, f"{player.display_name} swapped to {player.active_creature.display_name}!")

    def check_battle_end(self):
        player_creatures_alive = any(creature.hp > 0 for creature in self.player.creatures)
        opponent_creatures_alive = any(creature.hp > 0 for creature in self.opponent.creatures)

        if not player_creatures_alive:
            self.battle_result = "lose"
            return True
        elif not opponent_creatures_alive:
            self.battle_result = "win"
            return True
        return False

    def end_battle(self):
        if self.battle_result == "win":
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
        elif self.battle_result == "lose":
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
