from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
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
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                continue

            # Resolve actions
            self.resolve_turn(player_action, bot_action)

            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()

    def get_player_action(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            main_choice = self._wait_for_choice(current_player, [attack_button, swap_button])
            
            if main_choice == attack_button:
                # Show skills with Back option
                skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
                back_button = Button("Back")
                choice = self._wait_for_choice(current_player, skill_choices + [back_button])
                
                if choice == back_button:
                    continue  # Go back to main choices
                return choice
            else:
                # Show available creatures with Back option
                available_creatures = [c for c in current_player.creatures 
                                    if c.hp > 0 and c != current_player.active_creature]
                if not available_creatures:
                    return None
                    
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                back_button = Button("Back")
                choice = self._wait_for_choice(current_player, creature_choices + [back_button])
                
                if choice == back_button:
                    continue  # Go back to main choices
                return choice

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing

        # Then handle attacks
        first_player, first_action, second_player, second_action = self.determine_turn_order(
            self.player, player_action, self.bot, bot_action)
            
        if isinstance(first_action.thing, Creature):
            self._show_text(first_player, f"{first_player.display_name} swapped to {first_action.thing.display_name}!")
        else:
            self.execute_attack(first_player, second_player, first_action.thing)
            
        if isinstance(second_action.thing, Creature):
            self._show_text(second_player, f"{second_player.display_name} swapped to {second_action.thing.display_name}!")
        else:
            self.execute_attack(second_player, first_player, second_action.thing)

    def determine_turn_order(self, p1, p1_action, p2, p2_action):
        # Swaps always go first
        if isinstance(p1_action.thing, Creature):
            return p1, p1_action, p2, p2_action
        if isinstance(p2_action.thing, Creature):
            return p2, p2_action, p1, p1_action
            
        # Compare speeds
        if p1.active_creature.speed > p2.active_creature.speed:
            return p1, p1_action, p2, p2_action
        elif p2.active_creature.speed > p1.active_creature.speed:
            return p2, p2_action, p1, p1_action
        else:
            if random.random() < 0.5:
                return p1, p1_action, p2, p2_action
            return p2, p2_action, p1, p1_action

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage!")

        if defender.active_creature.hp == 0:
            self.handle_knockout(defender)

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def handle_knockout(self, player):
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing
            self._show_text(player, f"Go, {player.active_creature.display_name}!")

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
