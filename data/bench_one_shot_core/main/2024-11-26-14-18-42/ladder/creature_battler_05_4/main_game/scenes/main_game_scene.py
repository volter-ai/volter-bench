from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP" 
            for c in self.player.creatures
        )
        bot_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP"
            for c in self.bot.creatures
        )
        
        return f"""=== Battle Scene ===
Your Team:
{player_creatures_status}
Active: {self.player.active_creature.display_name}

Opponent's Team: 
{bot_creatures_status}
Active: {self.bot.active_creature.display_name}

> Attack - Use a skill
> Swap - Switch active creature (if available)
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_available_creatures(self, player):
        return [c for c in player.creatures 
                if c != player.active_creature and c.hp > 0]

    def get_player_action(self, player):
        # Main choice menu
        available_creatures = self.get_available_creatures(player)
        
        choices = [Button("Attack")]
        if available_creatures:
            choices.append(Button("Swap"))
        
        main_choice = self._wait_for_choice(player, choices)
        
        if main_choice.display_name == "Attack":
            # Show skills with Back option
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            skill_choices.append(Button("Back"))
            
            choice = self._wait_for_choice(player, skill_choices)
            if choice.display_name == "Back":
                return self.get_player_action(player)  # Go back to main choices
            return choice
            
        else:  # Swap
            # Show available creatures with Back option
            creature_choices = [SelectThing(c) for c in available_creatures]
            creature_choices.append(Button("Back"))
            
            choice = self._wait_for_choice(player, creature_choices)
            if choice.display_name == "Back":
                return self.get_player_action(player)  # Go back to main choices
            return choice

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            
        # Then handle attacks
        first_action, second_action = self.get_action_order(player_action, bot_action)
        self.execute_action(first_action, is_player_action=(first_action == player_action))
        self.execute_action(second_action, is_player_action=(second_action == player_action))

    def get_action_order(self, player_action, bot_action):
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_action, bot_action
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return bot_action, player_action
        else:
            return (player_action, bot_action) if random.random() > 0.5 else (bot_action, player_action)

    def execute_action(self, action, is_player_action: bool):
        if isinstance(action.thing, Creature):
            return # Swap already handled
            
        skill = action.thing
        attacker = self.player.active_creature if is_player_action else self.bot.active_creature
        defender = self.bot.active_creature if is_player_action else self.player.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {final_damage} damage!")
        
        if defender.hp == 0:
            self.handle_knockout(defender)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, knocked_out_creature):
        owner = self.player if knocked_out_creature in self.player.creatures else self.bot
        
        available_creatures = self.get_available_creatures(owner)
        if not available_creatures:
            return
            
        self._show_text(owner, f"{knocked_out_creature.display_name} was knocked out! Choose a new creature!")
        creature_choices = [SelectThing(c) for c in available_creatures]
        new_creature = self._wait_for_choice(owner, creature_choices).thing
        owner.active_creature = new_creature

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            winner = "You" if player_alive else "Opponent"
            self._show_text(self.player, f"{winner} won the battle!")
            
            # Reset creatures
            for c in self.player.creatures + self.bot.creatures:
                c.hp = c.max_hp
                
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
