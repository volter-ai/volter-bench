from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
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
            player_action = self._get_player_action(self.player)
            if not player_action:
                return
                
            # Bot turn
            bot_action = self._get_player_action(self.bot)
            if not bot_action:
                return

            # Resolve actions
            self._resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                return

    def _get_player_action(self, player):
        if not self._handle_fainted_creature(player):
            return None
            
        action_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [action_button, swap_button])
        
        if choice == action_button:
            return self._handle_attack_choice(player)
        else:
            return self._handle_swap_choice(player)

    def _handle_attack_choice(self, player):
        back_button = Button("Back")
        choices = [SelectThing(skill) for skill in player.active_creature.skills] + [back_button]
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self._get_player_action(player)
            
        return {"type": "attack", "skill": choice.thing}

    def _handle_swap_choice(self, player):
        back_button = Button("Back")
        valid_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(c) for c in valid_creatures] + [back_button]
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self._get_player_action(player)
            
        return {"type": "swap", "creature": choice.thing}

    def _handle_fainted_creature(self, player):
        if player.active_creature.hp <= 0:
            valid_creatures = [c for c in player.creatures if c.hp > 0]
            if not valid_creatures:
                return False
                
            choices = [SelectThing(c) for c in valid_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            
        return True

    def _resolve_actions(self, p_action, b_action):
        # Handle swaps first
        if p_action["type"] == "swap":
            self.player.active_creature = p_action["creature"]
        if b_action["type"] == "swap":
            self.bot.active_creature = b_action["creature"]
            
        # Then handle attacks
        first, second = self._determine_order(p_action, b_action)
        self._execute_action(first[0], first[1])
        if second[0].active_creature.hp > 0:  # Only execute second if target still alive
            self._execute_action(second[0], second[1])

    def _determine_order(self, p_action, b_action):
        p_speed = self.player.active_creature.speed
        b_speed = self.bot.active_creature.speed
        
        if p_speed > b_speed or (p_speed == b_speed and random.random() < 0.5):
            return (self.player, p_action), (self.bot, b_action)
        return (self.bot, b_action), (self.player, p_action)

    def _execute_action(self, attacker, action):
        if action["type"] != "attack":
            return
            
        defender = self.bot if attacker == self.player else self.player
        skill = action["skill"]
        target = defender.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - target.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / target.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, target.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        target.hp = max(0, target.hp - final_damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{target.display_name} took {final_damage} damage!")

    def _get_type_multiplier(self, skill_type, target_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(target_type, 1.0)

    def _reset_creatures(self):
        """Reset all creatures to their initial state"""
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

    def _check_battle_end(self):
        p_alive = any(c.hp > 0 for c in self.player.creatures)
        b_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_alive or not b_alive:
            winner = self.player if p_alive else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            # Reset creature states before transitioning
            self._reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
