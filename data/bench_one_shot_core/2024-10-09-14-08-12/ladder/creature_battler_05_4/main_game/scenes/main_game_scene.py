import random

from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.turn_order = [self.player, self.bot]
        self.initialize_battle()

    def initialize_battle(self):
        for player in self.turn_order:
            if player.creatures:
                player.active_creature = player.creatures[0]
            else:
                raise ValueError(f"Player {player.display_name} has no creatures!")

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name if self.player.active_creature else 'No active creature'} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} if self.player.active_creature else 'N/A')
{self.bot.display_name}: {self.bot.active_creature.display_name if self.bot.active_creature else 'No active creature'} (HP: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} if self.bot.active_creature else 'N/A')

> Attack
> Swap
"""

    def run(self):
        try:
            while True:
                action_queue = []
                for current_player in self.turn_order:
                    action = self.player_turn(current_player)
                    if action[0] == "quit":
                        return
                    action_queue.append((current_player, action))
                
                self.resolve_turn(action_queue)
                
                winner = self.check_battle_end()
                if winner:
                    self.inform_battle_result(winner)
                    return
        finally:
            self.reset_creatures_state()

    def player_turn(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if attack_button == choice:
                action = self.choose_attack(player)
            elif swap_button == choice:
                action = self.choose_swap(player)
            
            if action[0] != "back":
                return action

    def choose_attack(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices.append(back_button)
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            return ("back", None)
        return ("attack", choice.thing)

    def choose_swap(self, player):
        available_creatures = self.get_available_creatures(player)
        if not available_creatures:
            self._show_text(player, f"{player.display_name} has no creatures available to swap!")
            return ("no_op", None)
        
        choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices.append(back_button)
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            return ("back", None)
        return ("swap", choice.thing)

    def get_available_creatures(self, player):
        return [c for c in player.creatures if c != player.active_creature and c.hp > 0]

    def resolve_turn(self, action_queue):
        # Sort actions: swaps first, then by speed (randomly if equal)
        action_queue.sort(key=lambda x: (x[1][0] != "swap", -x[0].active_creature.speed, random.random()))

        for player, action in action_queue:
            if action[0] == "swap":
                player.active_creature = action[1]
                self._show_text(player, f"{player.display_name} swapped to {action[1].display_name}!")
            elif action[0] == "attack":
                self.execute_attack(player, action[1])
            elif action[0] == "no_op":
                self._show_text(player, f"{player.display_name} couldn't take any action this turn.")

        self.check_and_force_swap()

    def execute_attack(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5},
            "normal": {}  # Normal type is neutral against all types
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_and_force_swap(self):
        for player in self.turn_order:
            if player.active_creature.hp == 0:
                available_creatures = self.get_available_creatures(player)
                if available_creatures:
                    choices = [SelectThing(creature) for creature in available_creatures]
                    self._show_text(player, f"{player.active_creature.display_name} has fainted! Choose a new creature:")
                    choice = self._wait_for_choice(player, choices)
                    player.active_creature = choice.thing
                    self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")
                else:
                    self._show_text(player, f"{player.display_name} has no more creatures able to battle!")

    def check_battle_end(self):
        for player in self.turn_order:
            if all(creature.hp == 0 for creature in player.creatures):
                return self.bot if player == self.player else self.player
        return None

    def inform_battle_result(self, winner):
        if winner == self.player:
            self._show_text(self.player, "Congratulations! You won the battle!")
        else:
            self._show_text(self.player, "You lost the battle. Better luck next time!")

    def reset_creatures_state(self):
        for player in self.turn_order:
            for creature in player.creatures:
                creature.hp = creature.max_hp
        self._show_text(self.player, "All creatures have been restored to full health.")
