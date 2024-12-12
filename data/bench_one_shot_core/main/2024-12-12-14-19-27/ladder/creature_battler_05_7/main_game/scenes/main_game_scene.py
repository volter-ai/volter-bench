from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
        # Reset creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap
"""

    def get_available_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Calculate type multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": multiplier = 2.0
            elif defender.creature_type == "water": multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": multiplier = 2.0
            elif defender.creature_type == "leaf": multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": multiplier = 2.0
            elif defender.creature_type == "fire": multiplier = 0.5

        return int(raw_damage * multiplier)

    def handle_turn(self, player, opponent):
        # Get player action
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choice = self._wait_for_choice(player, [attack_button, swap_button])

        action = None
        if choice == attack_button:
            # Show skills
            back_button = Button("Back")
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills] + [back_button]
            skill_choice = self._wait_for_choice(player, skill_choices)
            if skill_choice != back_button:
                action = ("attack", skill_choice.thing)
        else:
            # Show available creatures
            available = self.get_available_creatures(player)
            back_button = Button("Back")
            creature_choices = [SelectThing(creature) for creature in available] + [back_button]
            creature_choice = self._wait_for_choice(player, creature_choices)
            if creature_choice != back_button:
                action = ("swap", creature_choice.thing)

        return action

    def execute_turn(self, first_action, second_action, first_player, second_player):
        # Handle swaps first
        if first_action and first_action[0] == "swap":
            first_player.active_creature = first_action[1]
        if second_action and second_action[0] == "swap":
            second_player.active_creature = second_action[1]

        # Handle attacks
        if first_action and first_action[0] == "attack":
            damage = self.calculate_damage(first_player.active_creature, second_player.active_creature, first_action[1])
            second_player.active_creature.hp -= damage
            self._show_text(first_player, f"{first_player.active_creature.display_name} used {first_action[1].display_name}!")
            self._show_text(first_player, f"Dealt {damage} damage!")

        if second_action and second_action[0] == "attack" and second_player.active_creature.hp > 0:
            damage = self.calculate_damage(second_player.active_creature, first_player.active_creature, second_action[1])
            first_player.active_creature.hp -= damage
            self._show_text(second_player, f"{second_player.active_creature.display_name} used {second_action[1].display_name}!")
            self._show_text(second_player, f"Dealt {damage} damage!")

    def handle_fainted(self, player):
        if player.active_creature.hp <= 0:
            available = self.get_available_creatures(player)
            if not available:
                return False
            
            creature_choices = [SelectThing(creature) for creature in available]
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing
            
        return True

    def run(self):
        while True:
            # Get actions
            player_action = self.handle_turn(self.player, self.bot)
            bot_action = self.handle_turn(self.bot, self.player)

            if not player_action or not bot_action:
                continue

            # Determine order
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                first, second = self.player, self.bot
                first_action, second_action = player_action, bot_action
            elif self.player.active_creature.speed < self.bot.active_creature.speed:
                first, second = self.bot, self.player
                first_action, second_action = bot_action, player_action
            else:
                if random.random() < 0.5:
                    first, second = self.player, self.bot
                    first_action, second_action = player_action, bot_action
                else:
                    first, second = self.bot, self.player
                    first_action, second_action = bot_action, player_action

            # Execute turn
            self.execute_turn(first_action, second_action, first, second)

            # Handle fainted creatures
            if not self.handle_fainted(self.player):
                self._show_text(self.player, "You lost!")
                break
            if not self.handle_fainted(self.bot):
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")
