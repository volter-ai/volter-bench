from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
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
        player_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP" 
            for c in self.player.creatures
        )
        bot_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP" 
            for c in self.bot.creatures
        )
        
        return f"""=== Battle ===
Your Team:
{player_creatures_status}
Active: {self.player.active_creature.display_name}

Opponent's Team:
{bot_creatures_status}
Active: {self.bot.active_creature.display_name}

> Attack
> Swap (if available)"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()

    def get_player_action(self, player):
        while True:
            # Main menu choices
            choices = [Button("Attack")]
            
            # Only add swap if there are valid creatures to swap to
            valid_swap_creatures = [
                c for c in player.creatures 
                if c != player.active_creature and c.hp > 0
            ]
            if valid_swap_creatures:
                choices.append(Button("Swap"))
            
            main_choice = self._wait_for_choice(player, choices)
            
            if main_choice.display_name == "Attack":
                # Attack submenu
                choices = [SelectThing(skill) for skill in player.active_creature.skills]
                choices.append(Button("Back"))
                
                attack_choice = self._wait_for_choice(player, choices)
                
                if isinstance(attack_choice, Button) and attack_choice.display_name == "Back":
                    continue  # Go back to main menu
                return attack_choice
                
            else:  # Swap
                # Swap submenu
                choices = [SelectThing(c) for c in valid_swap_creatures]
                choices.append(Button("Back"))
                
                swap_choice = self._wait_for_choice(player, choices)
                
                if isinstance(swap_choice, Button) and swap_choice.display_name == "Back":
                    continue  # Go back to main menu
                return swap_choice

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            
        # Then handle attacks
        actions = []
        if isinstance(player_action.thing, Skill):
            actions.append((self.player, player_action.thing))
        if isinstance(bot_action.thing, Skill):
            actions.append((self.bot, bot_action.thing))
            
        # Sort by speed
        actions.sort(
            key=lambda x: x[0].active_creature.speed,
            reverse=True
        )
        
        # Execute attacks
        for attacker, skill in actions:
            defender = self.bot if attacker == self.player else self.player
            self.execute_skill(attacker, defender, skill)
            
            # Force swap if needed
            if defender.active_creature.hp <= 0:
                valid_creatures = [
                    c for c in defender.creatures if c.hp > 0
                ]
                if valid_creatures:
                    choices = [SelectThing(c) for c in valid_creatures]
                    swap = self._wait_for_choice(defender, choices)
                    defender.active_creature = swap.thing

    def execute_skill(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = (
                attacker.active_creature.attack + 
                skill.base_damage - 
                defender.active_creature.defense
            )
        else:
            raw_damage = (
                skill.base_damage * 
                attacker.active_creature.sp_attack / 
                defender.active_creature.sp_defense
            )
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(
            skill.skill_type,
            defender.active_creature.creature_type
        )
        
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp -= max(1, final_damage)
        
        self._show_text(
            attacker,
            f"{attacker.active_creature.display_name} used {skill.display_name}!"
        )
        self._show_text(
            defender,
            f"{defender.active_creature.display_name} took {final_damage} damage!"
        )

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            winner = self.player if player_alive else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            return True
            
        return False
