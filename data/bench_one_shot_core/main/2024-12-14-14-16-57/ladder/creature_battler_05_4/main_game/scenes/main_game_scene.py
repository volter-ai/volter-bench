from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
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
> Swap (if available)"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # After showing win/loss message, ask player what to do next
                continue_button = Button("Continue")
                quit_button = Button("Quit")
                choice = self._wait_for_choice(self.player, [continue_button, quit_button])
                
                if choice == continue_button:
                    self._transition_to_scene("MainMenuScene")
                else:
                    self._quit_whole_game()
                return

    def get_player_action(self, player):
        # Get available creatures for swapping
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        
        # Build choice list based on available options
        choices = [Button("Attack")]
        if available_creatures:
            choices.append(Button("Swap"))
            
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            # Show skills with Back option
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            back_button = Button("Back")
            skill_choices.append(back_button)
            
            skill_choice = self._wait_for_choice(player, skill_choices)
            if skill_choice == back_button:
                return self.get_player_action(player)  # Go back to main choices
            return skill_choice
            
        else:  # Swap
            # Show available creatures with Back option
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            back_button = Button("Back")
            creature_choices.append(back_button)
            
            creature_choice = self._wait_for_choice(player, creature_choices)
            if creature_choice == back_button:
                return self.get_player_action(player)  # Go back to main choices
            return creature_choice

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            
        # Resolve attacks
        first, second = self.determine_order(player_action, bot_action)
        self.execute_action(first)
        self.execute_action(second)

    def determine_order(self, player_action, bot_action):
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_action, bot_action
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return bot_action, player_action
        else:
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def execute_action(self, action):
        if isinstance(action.thing, Creature):
            return
            
        skill = action.thing
        attacker = self.player if action.thing in self.player.active_creature.skills else self.bot
        defender = self.bot if attacker == self.player else self.player
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"It dealt {final_damage} damage!")

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def check_battle_end(self):
        def has_available_creatures(player):
            return any(c.hp > 0 for c in player.creatures)
            
        if not has_available_creatures(self.player):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not has_available_creatures(self.bot):
            self._show_text(self.player, "You won the battle!")
            return True
            
        if self.player.active_creature.hp == 0:
            available = [c for c in self.player.creatures if c.hp > 0]
            if available:
                swap_choices = [SelectThing(c) for c in available]
                choice = self._wait_for_choice(self.player, swap_choices)
                self.player.active_creature = choice.thing
                
        if self.bot.active_creature.hp == 0:
            available = [c for c in self.bot.creatures if c.hp > 0]
            if available:
                swap_choices = [SelectThing(c) for c in available]
                choice = self._wait_for_choice(self.bot, swap_choices)
                self.bot.active_creature = choice.thing
                
        return False
