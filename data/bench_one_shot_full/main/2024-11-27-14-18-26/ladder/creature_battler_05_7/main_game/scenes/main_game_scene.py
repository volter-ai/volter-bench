from typing import List, Dict, Tuple
import random
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, create_from_game_database
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        # Initialize active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

Available actions:
> Attack
{"> Swap" if self._get_available_creatures(self.player) else ""}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            if not self._check_can_continue():
                break
                
            # Player turn
            player_action = self._get_player_action(self.player)
            bot_action = self._get_player_action(self.bot)
            
            # Execute actions
            self._resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                break
                
        # Reset creatures before asking to play again
        self._reset_creatures()
        
        # Ask player if they want to play again
        play_again = Button("Play Again")
        quit_game = Button("Quit")
        choice = self._wait_for_choice(self.player, [play_again, quit_game])
        
        if choice == play_again:
            self._transition_to_scene("MainMenuScene")
        else:
            self._quit_whole_game()

    def _get_available_creatures(self, player: Player) -> List[Creature]:
        """Get list of creatures that can be swapped to"""
        return [
            creature for creature in player.creatures 
            if creature != player.active_creature and creature.hp > 0
        ]

    def _check_can_continue(self) -> bool:
        """Check if both players have creatures that can fight"""
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return False
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return False
            
        return True

    def _get_player_action(self, current_player: Player) -> Tuple[str, Skill | Creature]:
        choices = [Button("Attack")]
        
        # Only add swap option if there are creatures available to swap to
        available_creatures = self._get_available_creatures(current_player)
        if available_creatures:
            choices.append(Button("Swap"))
            
        choice = self._wait_for_choice(current_player, choices)
        
        if choice.display_name == "Attack":
            # Show skills
            skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
            skill_choice = self._wait_for_choice(current_player, skill_choices)
            return ("attack", skill_choice.thing)
        else:
            # Show available creatures
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            creature_choice = self._wait_for_choice(current_player, creature_choices)
            return ("swap", creature_choice.thing)

    def _resolve_turn(self, player_action: Tuple[str, Skill | Creature], bot_action: Tuple[str, Skill | Creature]):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            
        # Then handle attacks
        if player_action[0] == "attack" and bot_action[0] == "attack":
            # Determine order based on speed
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                self._execute_attack(self.player, self.bot, player_action[1])
                if self.bot.active_creature.hp > 0:
                    self._execute_attack(self.bot, self.player, bot_action[1])
            else:
                self._execute_attack(self.bot, self.player, bot_action[1])
                if self.player.active_creature.hp > 0:
                    self._execute_attack(self.player, self.bot, player_action[1])
        elif player_action[0] == "attack":
            self._execute_attack(self.player, self.bot, player_action[1])
        elif bot_action[0] == "attack":
            self._execute_attack(self.bot, self.player, bot_action[1])

    def _execute_attack(self, attacker: Player, defender: Player, skill: Skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show result
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}")
        
        # Handle knockout
        if defender.active_creature.hp == 0:
            self._handle_knockout(defender)

    def _get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def _handle_knockout(self, player: Player):
        self._show_text(self.player, f"{player.active_creature.display_name} was knocked out!")
        
        # Get available creatures
        available_creatures = self._get_available_creatures(player)
        
        if available_creatures:
            # Force swap
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            new_creature = self._wait_for_choice(player, creature_choices).thing
            player.active_creature = new_creature

    def _check_battle_end(self) -> bool:
        return not self._check_can_continue()

    def _reset_creatures(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
