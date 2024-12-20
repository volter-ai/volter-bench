from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
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

Your other creatures:
{self._format_bench(self.player)}

Foe's other creatures:
{self._format_bench(self.bot)}
"""

    def _format_bench(self, player):
        return "\n".join(f"- {c.display_name}: {c.hp}/{c.max_hp} HP" 
                        for c in player.creatures if c != player.active_creature)

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
            if not self._handle_forced_swap(player):
                return None
                
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self._handle_attack(player)
        else:
            return self._handle_swap(player)

    def _handle_attack(self, player):
        skills = [SelectThing(s) for s in player.active_creature.skills]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, skills + [back_button])
        
        if choice == back_button:
            return self._handle_turn(player)
            
        return ("attack", choice.thing)

    def _handle_swap(self, player):
        available = [SelectThing(c) for c in player.creatures 
                    if c != player.active_creature and c.hp > 0]
        back_button = Button("Back")
        
        if not available:
            self._show_text(player, "No creatures available to swap!")
            return self._handle_turn(player)
            
        choice = self._wait_for_choice(player, available + [back_button])
        
        if choice == back_button:
            return self._handle_turn(player)
            
        return ("swap", choice.thing)

    def _handle_forced_swap(self, player):
        available = [SelectThing(c) for c in player.creatures if c.hp > 0]
        
        if not available:
            self._show_text(player, f"{player.display_name} has no creatures left!")
            return False
            
        choice = self._wait_for_choice(player, available)
        player.active_creature = choice.thing
        return True

    def _resolve_actions(self, p_action, b_action):
        first_action, second_action = self._determine_order(p_action, b_action)
        
        # Execute first action
        self._execute_action(*first_action)
        # Execute second action
        self._execute_action(*second_action)

    def _determine_order(self, p_action, b_action):
        # Determine if player goes first
        p_first = True
        
        # Swaps go first
        if p_action[0] == "swap" and b_action[0] != "swap":
            p_first = True
        elif b_action[0] == "swap" and p_action[0] != "swap":
            p_first = False
        # Compare speeds for attacks
        elif p_action[0] == "attack" and b_action[0] == "attack":
            p_speed = self.player.active_creature.speed
            b_speed = self.bot.active_creature.speed
            if p_speed == b_speed:
                p_first = random.choice([True, False])
            else:
                p_first = p_speed > b_speed
        
        # Return actions in correct order with their actors
        if p_first:
            return (
                (p_action[0], p_action[1], self.player, self.bot),
                (b_action[0], b_action[1], self.bot, self.player)
            )
        else:
            return (
                (b_action[0], b_action[1], self.bot, self.player),
                (p_action[0], p_action[1], self.player, self.bot)
            )

    def _execute_action(self, action_type, action, attacker, defender):
        if action_type == "swap":
            attacker.active_creature = action
            self._show_text(attacker, f"{attacker.display_name} swapped to {action.display_name}!")
        else:
            damage = self._calculate_damage(action, attacker.active_creature, defender.active_creature)
            defender.active_creature.hp -= damage
            self._show_text(attacker, 
                f"{attacker.active_creature.display_name} used {action.display_name}! "
                f"Dealt {damage} damage!")

    def _calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * factor)

    def _get_type_factor(self, skill_type, defender_type):
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
            winner = self.bot if not p_alive else self.player
            self._show_text(self.player, f"{winner.display_name} wins!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
