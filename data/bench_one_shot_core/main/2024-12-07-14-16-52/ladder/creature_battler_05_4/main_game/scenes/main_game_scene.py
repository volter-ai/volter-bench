from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

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
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" 
                         for c in player.creatures if c != player.active_creature])

    def run(self):
        while True:
            # Player turn
            player_action = self._get_player_action(self.player)
            if not player_action:
                return
                
            # Bot turn
            bot_action = self._get_bot_action()
            
            # Resolve actions
            self._resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                # Reset creatures before ending
                for p in [self.player, self.bot]:
                    for c in p.creatures:
                        c.hp = c.max_hp
                self._quit_whole_game()  # Properly end the game
                return

    def _get_player_action(self, player):
        attack = Button("Attack")
        swap = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack, swap])
        
        if choice == attack:
            skills = [SelectThing(s) for s in player.active_creature.skills]
            back = Button("Back")
            skill_choice = self._wait_for_choice(player, skills + [back])
            if skill_choice == back:
                return self._get_player_action(player)
            return {"type": "attack", "skill": skill_choice.thing}
            
        elif choice == swap:
            available = [SelectThing(c) for c in player.creatures 
                        if c != player.active_creature and c.hp > 0]
            if not available:
                self._show_text(player, "No creatures available to swap!")
                return self._get_player_action(player)
                
            back = Button("Back")
            swap_choice = self._wait_for_choice(player, available + [back])
            if swap_choice == back:
                return self._get_player_action(player)
            return {"type": "swap", "creature": swap_choice.thing}

    def _get_bot_action(self):
        # Simple bot AI - randomly attack or swap
        if random.random() < 0.8:  # 80% chance to attack
            skill = random.choice(self.bot.active_creature.skills)
            return {"type": "attack", "skill": skill}
        else:
            available = [c for c in self.bot.creatures 
                        if c != self.bot.active_creature and c.hp > 0]
            if available:
                return {"type": "swap", "creature": random.choice(available)}
            return {"type": "attack", "skill": random.choice(self.bot.active_creature.skills)}

    def _resolve_actions(self, p_action, b_action):
        # Handle swaps first
        if p_action["type"] == "swap":
            self.player.active_creature = p_action["creature"]
        if b_action["type"] == "swap":
            self.bot.active_creature = b_action["creature"]
            
        # Then handle attacks
        if p_action["type"] == "attack" and b_action["type"] == "attack":
            # Determine order
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                first, second = (self.player, p_action), (self.bot, b_action)
            elif self.player.active_creature.speed < self.bot.active_creature.speed:
                first, second = (self.bot, b_action), (self.player, p_action)
            else:
                if random.random() < 0.5:
                    first, second = (self.player, p_action), (self.bot, b_action)
                else:
                    first, second = (self.bot, b_action), (self.player, p_action)
                    
            self._execute_attack(first[0], first[1]["skill"])
            if second[0].active_creature.hp > 0:  # Only counter if still alive
                self._execute_attack(second[0], second[1]["skill"])

    def _execute_attack(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         defender.active_creature.defense)
        else:
            raw_damage = (skill.base_damage * 
                         attacker.active_creature.sp_attack / 
                         defender.active_creature.sp_defense)
            
        # Apply type effectiveness
        factor = self._get_type_factor(skill.skill_type, 
                                     defender.active_creature.creature_type)
        
        final_damage = int(raw_damage * factor)
        defender.active_creature.hp = max(0, 
                                        defender.active_creature.hp - final_damage)
        
        # Show attack result
        self._show_text(self.player, 
                       f"{attacker.active_creature.display_name} used {skill.display_name}!")
        if factor > 1:
            self._show_text(self.player, "It's super effective!")
        elif factor < 1:
            self._show_text(self.player, "It's not very effective...")
            
        # Handle fainting
        if defender.active_creature.hp <= 0:
            self._show_text(self.player, 
                          f"{defender.active_creature.display_name} fainted!")
            self._handle_faint(defender)

    def _get_type_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _handle_faint(self, player):
        available = [c for c in player.creatures if c.hp > 0]
        if not available:
            return
            
        if player == self.player:
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
        else:
            player.active_creature = random.choice(available)

    def _check_battle_end(self):
        p_alive = any(c.hp > 0 for c in self.player.creatures)
        b_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_alive or not b_alive:
            if p_alive:
                self._show_text(self.player, "You won!")
            else:
                self._show_text(self.player, "You lost!")
            return True
        return False
