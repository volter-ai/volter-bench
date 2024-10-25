from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.turn_queue = []

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.opponent.display_name}'s {opponent_creature.display_name}: HP {opponent_creature.hp}/{opponent_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._show_text(self.player, "Battle start!")
        self._show_text(self.opponent, "Battle start!")
        
        battle_ended = False
        while not battle_ended:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()
            
            battle_ended = self.check_battle_end()

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        self.get_player_action(self.player)

    def foe_choice_phase(self):
        self.get_player_action(self.opponent)

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if choice == attack_button:
                skill = self.choose_skill(player)
                if skill:
                    self.turn_queue.append(("attack", player, skill))
                    return
            elif choice == swap_button:
                new_creature = self.choose_swap_creature(player)
                if new_creature:
                    self.turn_queue.append(("swap", player, new_creature))
                    return
                elif new_creature is None:
                    self._show_text(player, "No available creatures to swap!")

    def choose_skill(self, player):
        back_button = Button("Back")
        choices = [SelectThing(skill) for skill in player.active_creature.skills] + [back_button]
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return None
        return choice.thing

    def choose_swap_creature(self, player):
        available_creatures = [creature for creature in player.creatures if creature != player.active_creature and creature.hp > 0]
        if not available_creatures:
            return None
        back_button = Button("Back")
        choices = [SelectThing(creature) for creature in available_creatures] + [back_button]
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return False
        return choice.thing

    def resolution_phase(self):
        # Group actions by speed
        speed_groups = {}
        for action in self.turn_queue:
            speed = -1 if action[0] == "swap" else action[1].active_creature.speed
            if speed not in speed_groups:
                speed_groups[speed] = []
            speed_groups[speed].append(action)

        # Sort speeds in descending order
        sorted_speeds = sorted(speed_groups.keys(), reverse=True)

        # Execute actions
        for speed in sorted_speeds:
            # Randomize order within each speed group
            random.shuffle(speed_groups[speed])
            for action, player, target in speed_groups[speed]:
                opponent = self.opponent if player == self.player else self.player
                if action == "swap":
                    player.active_creature = target
                    self._show_text(self.player, f"{player.display_name} swapped to {target.display_name}!")
                    self._show_text(self.opponent, f"{player.display_name} swapped to {target.display_name}!")
                elif action == "attack":
                    self.execute_attack(player, opponent, target)

        self.turn_queue.clear()

    def execute_attack(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * type_factor)

        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)

        self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.opponent, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage to {defender.display_name}'s {defender.active_creature.display_name}!")
        self._show_text(self.opponent, f"It dealt {final_damage} damage to {defender.display_name}'s {defender.active_creature.display_name}!")

        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
            self._show_text(self.opponent, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
            self.force_swap(defender)

    def get_type_factor(self, skill_type, creature_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            new_creature = self.choose_swap_creature(player)
            if new_creature:
                player.active_creature = new_creature
                self._show_text(self.player, f"{player.display_name} sent out {new_creature.display_name}!")
                self._show_text(self.opponent, f"{player.display_name} sent out {new_creature.display_name}!")

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
