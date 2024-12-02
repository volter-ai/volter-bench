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
            if self.check_battle_end():
                self._transition_to_scene("MainMenuScene")
                return
                
            # Handle knocked out creatures before getting actions
            if self.player.active_creature.hp == 0:
                if not self.handle_knocked_out_creature(self.player):
                    self._show_text(self.player, "You lost the battle!")
                    self._transition_to_scene("MainMenuScene")
                    return
            if self.bot.active_creature.hp == 0:
                if not self.handle_knocked_out_creature(self.bot):
                    self._show_text(self.player, "You won the battle!")
                    self._transition_to_scene("MainMenuScene")
                    return
            
            # Get and resolve actions
            player_action = self.get_player_action(self.player)
            if player_action is None:  # Player chose "Back"
                continue
                
            bot_action = self.get_player_action(self.bot)
            self.resolve_turn(player_action, bot_action)

    def get_player_action(self, player):
        while True:
            # Only offer swap if there are creatures to swap to
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            
            choices = [Button("Attack")]
            if available_creatures:
                choices.append(Button("Swap"))
                
            choice = self._wait_for_choice(player, choices)
            
            if choice.display_name == "Attack":
                # Show skills with Back option
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(Button("Back"))
                choice = self._wait_for_choice(player, skill_choices)
                
                if choice.display_name == "Back":
                    continue  # Go back to main action menu
                return choice
            else:
                # Show available creatures with Back option
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choices.append(Button("Back"))
                choice = self._wait_for_choice(player, creature_choices)
                
                if choice.display_name == "Back":
                    continue  # Go back to main action menu
                return choice

    def handle_knocked_out_creature(self, player):
        available = [c for c in player.creatures if c.hp > 0]
        if not available:
            return False
            
        swap_choices = [SelectThing(c) for c in available]
        choice = self._wait_for_choice(player, swap_choices)
        player.active_creature = choice.thing
        return True

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            
        # Then handle attacks
        first, second = self.determine_order(player_action, bot_action)
        self.execute_action(first)
        if not isinstance(second.thing, Creature):  # Only execute attack if it's not a swap
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
            
        return False
