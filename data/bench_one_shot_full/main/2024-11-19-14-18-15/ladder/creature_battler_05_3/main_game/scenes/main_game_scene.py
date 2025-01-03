from typing import Dict, Tuple, Optional
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, AbstractPlayer
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app=app, player=player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creatures by setting hp to max_hp
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures    
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

Your Team:
{self._format_team(self.player)}

Foe's Team:
{self._format_team(self.bot)}
"""

    def _format_team(self, player):
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" for c in player.creatures])

    def run(self):
        while True:
            # Player turn
            player_action = self._handle_turn(self.player)
            if not player_action:
                return
                
            # Bot turn
            bot_action = self._handle_turn(self.bot)
            if not bot_action:
                return
                
            # Resolve actions
            self._resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                return

    def _handle_turn(self, player) -> Optional[Dict]:
        if player.active_creature.hp <= 0:
            if not self._handle_forced_swap(player):
                return None
                
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self._handle_attack(player)
        else:
            return self._handle_swap(player)

    def _handle_attack(self, player) -> Optional[Dict]:
        skills = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, skills + [back_button])
        
        if choice == back_button:
            return self._handle_turn(player)
            
        return {"type": "attack", "skill": choice.thing}

    def _handle_swap(self, player) -> Optional[Dict]:
        available_creatures = [
            SelectThing(c) for c in player.creatures 
            if c != player.active_creature and c.hp > 0
        ]
        back_button = Button("Back")
        
        if not available_creatures:
            self._show_text(player, "No creatures available to swap!")
            return self._handle_turn(player)
            
        choice = self._wait_for_choice(player, available_creatures + [back_button])
        
        if choice == back_button:
            return self._handle_turn(player)
            
        return {"type": "swap", "creature": choice.thing}

    def _handle_forced_swap(self, player) -> bool:
        available_creatures = [
            SelectThing(c) for c in player.creatures 
            if c.hp > 0
        ]
        
        if not available_creatures:
            return False
            
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        choice = self._wait_for_choice(player, available_creatures)
        
        player.active_creature = choice.thing
        return True

    def _resolve_actions(self, player_action: Dict, bot_action: Dict) -> None:
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"You swapped to {player_action['creature'].display_name}!")
            
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            self._show_text(self.player, f"Foe swapped to {bot_action['creature'].display_name}!")
            
        # Then handle attacks
        if player_action["type"] == "attack" and bot_action["type"] == "attack":
            first_player, first_action = self._determine_order(
                (self.player, player_action), 
                (self.bot, bot_action)
            )
            self._execute_attack(first_player, first_action)
            
            second_player = self.bot if first_player == self.player else self.player
            second_action = bot_action if first_player == self.player else player_action
            
            if second_action["type"] == "attack" and second_player.active_creature.hp > 0:
                self._execute_attack(second_player, second_action)

    def _determine_order(self, action1: Tuple[AbstractPlayer, Dict], action2: Tuple[AbstractPlayer, Dict]) -> Tuple[AbstractPlayer, Dict]:
        player1, action1 = action1
        player2, action2 = action2
        
        speed1 = player1.active_creature.speed
        speed2 = player2.active_creature.speed
        
        if speed1 > speed2:
            return player1, action1
        elif speed2 > speed1:
            return player2, action2
        else:
            return random.choice([(player1, action1), (player2, action2)])

    def _execute_attack(self, attacker: AbstractPlayer, action: Dict) -> None:
        skill = action["skill"]
        defender = self.bot if attacker == self.player else self.player
        
        # Calculate damage
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
        multiplier = self._get_type_multiplier(
            skill.skill_type,
            defender.active_creature.creature_type
        )
        
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp -= final_damage
        
        if defender.active_creature.hp < 0:
            defender.active_creature.hp = 0
            
        self._show_text(
            self.player,
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}!"
        )

    def _get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        if not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene") 
            return True
            
        return False
