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
                self._quit_whole_game()
                return
                
            # Bot turn
            bot_action = self._handle_turn(self.bot)
            if not bot_action:
                self._quit_whole_game()
                return
                
            # Resolve actions
            self._resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                self._quit_whole_game()
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
            
        return {"type": "attack", "skill": choice.thing}

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
            
        return {"type": "swap", "creature": choice.thing}

    def _handle_forced_swap(self, player):
        available = [SelectThing(c) for c in player.creatures 
                    if c != player.active_creature and c.hp > 0]
                    
        if not available:
            return False
            
        choice = self._wait_for_choice(player, available)
        player.active_creature = choice.thing
        return True

    def _resolve_actions(self, p_action, b_action):
        # Handle swaps first
        if p_action["type"] == "swap":
            self.player.active_creature = p_action["creature"]
        if b_action["type"] == "swap":
            self.bot.active_creature = b_action["creature"]
            
        # Then handle attacks
        if p_action["type"] == "attack" and b_action["type"] == "attack":
            first, second = self._determine_order(
                (self.player, p_action), 
                (self.bot, b_action)
            )
            self._execute_attack(*first)
            if second[0].active_creature.hp > 0:
                self._execute_attack(*second)

    def _determine_order(self, p_pair, b_pair):
        p_speed = p_pair[0].active_creature.speed
        b_speed = b_pair[0].active_creature.speed
        
        if p_speed > b_speed:
            return p_pair, b_pair
        elif b_speed > p_speed:
            return b_pair, p_pair
        else:
            pairs = [p_pair, b_pair]
            random.shuffle(pairs)
            return pairs[0], pairs[1]

    def _execute_attack(self, attacker, action):
        defender = self.bot if attacker == self.player else self.player
        skill = action["skill"]
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         defender.active_creature.defense)
        else:
            raw_damage = (attacker.active_creature.sp_attack / 
                         defender.active_creature.sp_defense * 
                         skill.base_damage)
            
        # Apply type effectiveness
        factor = self._get_type_factor(skill.skill_type, 
                                     defender.active_creature.creature_type)
        
        final_damage = int(raw_damage * factor)
        defender.active_creature.hp -= max(1, final_damage)
        
        self._show_text(attacker, 
            f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender,
            f"{defender.active_creature.display_name} took {final_damage} damage!")

    def _get_type_factor(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def _check_battle_end(self):
        p_alive = any(c.hp > 0 for c in self.player.creatures)
        b_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_alive or not b_alive:
            winner = self.player if p_alive else self.bot
            self._show_text(self.player, 
                "You win!" if winner == self.player else "You lose!")
            return True
            
        return False
