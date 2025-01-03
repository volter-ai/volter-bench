from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, create_from_game_database
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures for both players
        for p in [self.player, self.bot]:
            p.active_creature = p.creatures[0]
            for c in p.creatures:
                c.hp = c.max_hp

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

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

    def _handle_turn(self, player):
        if player.active_creature.hp <= 0:
            available = [c for c in player.creatures if c.hp > 0]
            if not available:
                self._show_text(self.player, f"{player.display_name} has no creatures left!")
                return None
                
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            return ("swap", choice.thing)
            
        while True:  # Main action loop
            attack = Button("Attack")
            swap = Button("Swap")
            choice = self._wait_for_choice(player, [attack, swap])
            
            if choice == attack:
                # Attack submenu
                skills = [SelectThing(s) for s in player.active_creature.skills]
                back = Button("Back")
                skill_choice = self._wait_for_choice(player, skills + [back])
                
                if skill_choice == back:
                    continue  # Return to main menu
                    
                return ("attack", skill_choice.thing)
                
            else:  # Swap chosen
                available = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                if not available:
                    self._show_text(self.player, "No other creatures available!")
                    continue
                
                choices = [SelectThing(c) for c in available]
                back = Button("Back")
                swap_choice = self._wait_for_choice(player, choices + [back])
                
                if swap_choice == back:
                    continue  # Return to main menu
                    
                player.active_creature = swap_choice.thing
                return ("swap", swap_choice.thing)

    def _resolve_actions(self, p_action, b_action):
        # Handle swaps first
        if p_action[0] == "swap":
            self._show_text(self.player, f"You swapped to {p_action[1].display_name}!")
        if b_action[0] == "swap":
            self._show_text(self.player, f"Foe swapped to {b_action[1].display_name}!")
            
        # Then handle attacks
        actions = []
        if p_action[0] == "attack":
            actions.append((self.player, p_action[1]))
        if b_action[0] == "attack":
            actions.append((self.bot, b_action[1]))
            
        # Sort by speed, using random tiebreaker for equal speeds
        actions.sort(key=lambda x: (x[0].active_creature.speed, random.random()), reverse=True)
        
        for attacker, skill in actions:
            defender = self.bot if attacker == self.player else self.player
            self._execute_skill(attacker, defender, skill)

    def _execute_skill(self, attacker, defender, skill):
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
        
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}!")

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _check_battle_end(self):
        p_alive = any(c.hp > 0 for c in self.player.creatures)
        b_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_alive or not b_alive:
            winner = self.player if p_alive else self.bot
            self._show_text(self.player, f"{winner.display_name} wins the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
