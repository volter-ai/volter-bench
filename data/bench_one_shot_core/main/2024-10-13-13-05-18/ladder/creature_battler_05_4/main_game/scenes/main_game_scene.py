import random
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.turn_counter = 0
        self.battle_ended = False

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
        
        while not self.battle_ended:
            self.turn_counter += 1
            player_action = self.player_choice_phase(self.player)
            opponent_action = self.player_choice_phase(self.opponent)
            self.resolution_phase(player_action, opponent_action)
            
            if self.check_battle_end():
                self.battle_ended = True
                self.show_battle_result()

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if attack_button == choice:
                attack_action = self.choose_attack(current_player)
                if attack_action:
                    return attack_action
            elif swap_button == choice:
                swap_action = self.choose_swap(current_player)
                if swap_action:
                    return swap_action

    def choose_attack(self, current_player):
        skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
        back_button = Button("Back")
        choices = skill_choices + [back_button]
        choice = self._wait_for_choice(current_player, choices)
        
        if choice == back_button:
            return None
        return ("attack", choice.thing)

    def choose_swap(self, current_player):
        available_creatures = [creature for creature in current_player.creatures if creature.hp > 0 and creature != current_player.active_creature]
        if not available_creatures:
            self._show_text(current_player, "No creatures available to swap.")
            return None
        
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices = creature_choices + [back_button]
        choice = self._wait_for_choice(current_player, choices)
        
        if choice == back_button:
            return None
        return ("swap", choice.thing)

    def resolution_phase(self, player_action, opponent_action):
        actions = [
            (self.player, player_action),
            (self.opponent, opponent_action)
        ]
        
        # Sort actions based on speed (swap always goes first)
        # Use random tiebreaker for same speed
        actions.sort(key=lambda x: (
            x[1][0] != "swap",
            -x[0].active_creature.speed,
            random.random()
        ))

        for current_player, action in actions:
            if action is None:
                continue
            other_player = self.opponent if current_player == self.player else self.player
            
            if action[0] == "swap":
                self.perform_swap(current_player, action[1])
            elif action[0] == "attack":
                self.perform_attack(current_player, other_player, action[1])

            if self.check_battle_end():
                return

    def perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")
        self._show_text(self.opponent, f"{player.display_name} swapped to {new_creature.display_name}!")

    def perform_attack(self, attacker, defender, skill):
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.opponent, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} took {damage} damage!")
        self._show_text(self.opponent, f"{defender.display_name}'s {defender.active_creature.display_name} took {damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
            self._show_text(self.opponent, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
            self.force_swap(defender)

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

    def force_swap(self, player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if not available_creatures:
            return

        creature_choices = [SelectThing(creature) for creature in available_creatures]
        new_creature = self._wait_for_choice(player, creature_choices).thing
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} sent out {new_creature.display_name}!")
        self._show_text(self.opponent, f"{player.display_name} sent out {new_creature.display_name}!")

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

    def show_battle_result(self):
        result = "won" if any(creature.hp > 0 for creature in self.player.creatures) else "lost"
        self._show_text(self.player, f"You have {result} the battle!")
        continue_button = Button("Continue")
        self._wait_for_choice(self.player, [continue_button])

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
