from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, create_from_game_database
from main_game.models import Player, Creature
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

Your other creatures: {[c.display_name for c in self.player.creatures if c != p_creature and c.hp > 0]}
Foe's other creatures: {[c.display_name for c in self.bot.creatures if c != b_creature and c.hp > 0]}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_action = self.get_player_action(self.player)
            if not player_action:
                return
                
            # Bot Choice Phase  
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                return

            # Resolution Phase
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                return

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skills = [SelectThing(s) for s in player.active_creature.skills]
            back_button = Button("Back")
            skill_choice = self._wait_for_choice(player, skills + [back_button])
            
            if skill_choice == back_button:
                return self.get_player_action(player)
                
            return ("skill", skill_choice.thing)
            
        else:
            # Show available creatures
            available = [SelectThing(c) for c in player.creatures 
                       if c != player.active_creature and c.hp > 0]
            back_button = Button("Back")
            
            if not available:
                self._show_text(player, "No creatures available to swap to!")
                return self.get_player_action(player)
                
            swap_choice = self._wait_for_choice(player, available + [back_button])
            
            if swap_choice == back_button:
                return self.get_player_action(player)
                
            return ("swap", swap_choice.thing)

    def resolve_actions(self, p_action, b_action):
        # Handle swaps first
        if p_action[0] == "swap":
            self.player.active_creature = p_action[1]
            self._show_text(self.player, f"You swapped to {p_action[1].display_name}!")
            
        if b_action[0] == "swap":
            self.bot.active_creature = b_action[1]
            self._show_text(self.player, f"Foe swapped to {b_action[1].display_name}!")

        # Then handle attacks
        if p_action[0] == "skill" and b_action[0] == "skill":
            # Determine order
            p_first = True
            if self.player.active_creature.speed == self.bot.active_creature.speed:
                p_first = random.choice([True, False])
            elif self.player.active_creature.speed < self.bot.active_creature.speed:
                p_first = False
                
            first = (self.player, p_action[1]) if p_first else (self.bot, b_action[1])
            second = (self.bot, b_action[1]) if p_first else (self.player, p_action[1])
            
            self.execute_skill(first[0], first[1])
            if second[0].active_creature.hp > 0:  # Only if target still alive
                self.execute_skill(second[0], second[1])

    def execute_skill(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}!")
        
        # Handle fainting
        if defender.active_creature.hp <= 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} was knocked out!")
            self.handle_knockout(defender)

    def get_type_effectiveness(self, skill_type, target_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(target_type, 1.0)

    def handle_knockout(self, player):
        available = [c for c in player.creatures if c.hp > 0]
        if not available:
            return
            
        if player == self.player:
            self._show_text(self.player, "Choose your next creature!")
            choice = self._wait_for_choice(player, [SelectThing(c) for c in available])
            player.active_creature = choice.thing
        else:
            player.active_creature = available[0]
            self._show_text(self.player, f"Foe sent out {player.active_creature.display_name}!")

    def check_battle_end(self):
        p_alive = any(c.hp > 0 for c in self.player.creatures)
        b_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_alive or not b_alive:
            self._show_text(self.player, "You won!" if p_alive else "You lost!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
