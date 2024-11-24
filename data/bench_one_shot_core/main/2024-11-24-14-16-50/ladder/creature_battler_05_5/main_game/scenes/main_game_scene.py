from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.turn_count = 0

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Turn {self.turn_count}

{self.bot.display_name}'s {bot_creature.display_name}
HP: {bot_creature.hp}/{bot_creature.max_hp}

{self.player.display_name}'s {player_creature.display_name}
HP: {player_creature.hp}/{player_creature.max_hp}

> Attack
> Swap"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self.game_loop()

    def game_loop(self):
        while True:
            # Player Choice Phase
            player_action = self.get_player_action(self.player)
            if not player_action:
                return

            # Bot Choice Phase  
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                return

            # Resolution Phase
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                return

            self.turn_count += 1

    def get_player_action(self, current_player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(current_player, [attack_button, swap_button])

        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
            back_button = Button("Back")
            skill_choice = self._wait_for_choice(current_player, skill_choices + [back_button])
            
            if skill_choice == back_button:
                return self.get_player_action(current_player)
            
            return ("attack", skill_choice.thing)

        elif choice == swap_button:
            # Show available creatures
            available_creatures = [c for c in current_player.creatures 
                                if c != current_player.active_creature and c.hp > 0]
            
            if not available_creatures:
                self._show_text(current_player, "No creatures available to swap!")
                return self.get_player_action(current_player)

            creature_choices = [SelectThing(creature) for creature in available_creatures]
            back_button = Button("Back")
            creature_choice = self._wait_for_choice(current_player, creature_choices + [back_button])

            if creature_choice == back_button:
                return self.get_player_action(current_player)

            return ("swap", creature_choice.thing)

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"{self.player.display_name} swapped to {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"{self.bot.display_name} swapped to {bot_action[1].display_name}!")

        # Then handle attacks
        if player_action[0] == "attack" and bot_action[0] == "attack":
            # Determine order based on speed
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                first, second = (self.player, player_action[1]), (self.bot, bot_action[1])
            elif self.player.active_creature.speed < self.bot.active_creature.speed:
                first, second = (self.bot, bot_action[1]), (self.player, player_action[1])
            else:
                if random.random() < 0.5:
                    first, second = (self.player, player_action[1]), (self.bot, bot_action[1])
                else:
                    first, second = (self.bot, bot_action[1]), (self.player, player_action[1])

            self.execute_attack(first[0], first[1])
            if self.bot.active_creature.hp > 0 and self.player.active_creature.hp > 0:
                self.execute_attack(second[0], second[1])

    def execute_attack(self, attacker, skill):
        if attacker == self.player:
            defender = self.bot
        else:
            defender = self.player

        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)

        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}!")

        if defender.active_creature.hp <= 0:
            self.handle_knockout(defender)

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)

    def handle_knockout(self, player):
        self._show_text(self.player, f"{player.active_creature.display_name} was knocked out!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        self._show_text(self.player, f"{player.display_name} sent out {choice.thing.display_name}!")

    def reset_creatures(self):
        """Reset all creatures to their initial state"""
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)

        if not player_has_creatures or not bot_has_creatures:
            if not player_has_creatures:
                self._show_text(self.player, "You lost the battle!")
            else:
                self._show_text(self.player, "You won the battle!")
            
            # Reset creatures before transitioning
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
