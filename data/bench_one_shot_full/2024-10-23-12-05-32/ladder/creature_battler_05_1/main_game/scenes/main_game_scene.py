from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, RandomModeGracefulExit


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.turn_counter = 0

    def __str__(self):
        return f"""===Main Game===
Turn: {self.turn_counter}

{self.player.display_name}:
Active Creature: {self.player.active_creature.display_name}
HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp}

{self.opponent.display_name}:
Active Creature: {self.opponent.active_creature.display_name}
HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        try:
            self._show_text(self.player, "Battle Start!")
            self._show_text(self.opponent, "Battle Start!")

            while True:
                self.turn_counter += 1
                player_action = self.player_turn(self.player)
                opponent_action = self.player_turn(self.opponent)

                self.resolve_turn(player_action, opponent_action)

                if self.check_battle_end():
                    break

            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
        except RandomModeGracefulExit:
            self._quit_whole_game()

    def player_turn(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if attack_button == choice:
                return self.choose_attack(current_player)
            elif swap_button == choice:
                return self.choose_swap(current_player)

    def choose_attack(self, current_player):
        skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
        back_button = Button("Back")
        choices = skill_choices + [back_button]
        choice = self._wait_for_choice(current_player, choices)

        if choice == back_button:
            return self.player_turn(current_player)
        return ("attack", choice.thing)

    def choose_swap(self, current_player):
        available_creatures = [creature for creature in current_player.creatures if creature.hp > 0 and creature != current_player.active_creature]
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices = creature_choices + [back_button]
        choice = self._wait_for_choice(current_player, choices)

        if choice == back_button:
            return self.player_turn(current_player)
        return ("swap", choice.thing)

    def resolve_turn(self, player_action, opponent_action):
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)

        for current_player, action in actions:
            if action[0] == "swap":
                self.perform_swap(current_player, action[1])
            elif action[0] == "attack":
                self.perform_attack(current_player, action[1])

    def perform_swap(self, current_player, new_creature):
        current_player.active_creature = new_creature
        self._show_text(self.player, f"{current_player.display_name} swapped to {new_creature.display_name}!")
        self._show_text(self.opponent, f"{current_player.display_name} swapped to {new_creature.display_name}!")

    def perform_attack(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)

        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")
        self._show_text(self.opponent, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} fainted!")
            self._show_text(self.opponent, f"{defender.active_creature.display_name} fainted!")
            self.force_swap(defender)

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)

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

    def force_swap(self, player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if not available_creatures:
            return

        creature_choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, creature_choices)
        self.perform_swap(player, choice.thing)

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            return True
        return False

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
