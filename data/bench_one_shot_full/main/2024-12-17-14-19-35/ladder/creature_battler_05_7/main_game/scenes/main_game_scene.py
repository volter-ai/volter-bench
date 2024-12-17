from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
from typing import Tuple, Optional

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creatures' HP to max_hp
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

Your team:
{self._format_team(self.player)}

Foe's team:
{self._format_team(self.bot)}
"""

    def _format_team(self, player):
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" for c in player.creatures])

    def run(self):
        while True:
            # Show current state
            self._show_text(self.player, str(self))
            
            # Get actions from both players
            player_action = self._get_player_action(self.player)
            if player_action is None:  # No valid actions available
                self._end_battle()
                return
                
            bot_action = self._get_player_action(self.bot)
            if bot_action is None:  # No valid actions available
                self._end_battle()
                return
            
            # Resolve actions
            self._resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                self._end_battle()
                return

    def _get_player_action(self, player):
        if player.active_creature.hp <= 0:
            return self._force_swap(player)
            
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self._handle_attack_choice(player)
        else:
            return self._handle_swap_choice(player)

    def _handle_attack_choice(self, player):
        back_button = Button("Back")
        choices = [SelectThing(skill) for skill in player.active_creature.skills] + [back_button]
        
        while True:
            choice = self._wait_for_choice(player, choices)
            if choice == back_button:
                return self._get_player_action(player)
            return ("attack", choice.thing)

    def _handle_swap_choice(self, player):
        back_button = Button("Back")
        valid_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in valid_creatures] + [back_button]
        
        if not valid_creatures:
            return self._get_player_action(player)
            
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self._get_player_action(player)
        return ("swap", choice.thing)

    def _force_swap(self, player):
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        if not valid_creatures:
            return None
        
        choices = [SelectThing(creature) for creature in valid_creatures]
        choice = self._wait_for_choice(player, choices)
        return ("swap", choice.thing)

    def _resolve_actions(self, player_action, bot_action):
        if not player_action or not bot_action:
            return
            
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            
        # Then handle attacks
        if player_action[0] == "attack" and bot_action[0] == "attack":
            # Create action tuples with (player, skill)
            player_attack = (self.player, player_action[1])
            bot_attack = (self.bot, bot_action[1])
            
            # Determine order
            first, second = self._determine_order(player_attack, bot_attack)
            
            # Execute first attack
            attacker, skill = first
            self._execute_attack(attacker, skill)
            
            # Execute second attack only if the attacker's creature is still alive
            attacker, skill = second
            if attacker.active_creature.hp > 0:
                self._execute_attack(attacker, skill)

    def _determine_order(self, action1: Tuple, action2: Tuple) -> Tuple:
        speed1 = action1[0].active_creature.speed
        speed2 = action2[0].active_creature.speed
        
        if speed1 > speed2:
            return action1, action2
        elif speed2 > speed1:
            return action2, action1
        else:
            return (action1, action2) if random.random() < 0.5 else (action2, action1)

    def _execute_attack(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        
        # Calculate damage
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
        
        return not player_has_creatures or not bot_has_creatures

    def _end_battle(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        winner = "You win!" if player_has_creatures else "You lose!"
        self._show_text(self.player, f"Battle Over! {winner}")
        self._transition_to_scene("MainMenuScene")
