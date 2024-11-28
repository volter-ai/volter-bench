from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Creature, Player
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

Your Team: {', '.join(c.display_name + f'({c.hp}/{c.max_hp})' for c in self.player.creatures)}
Foe's Team: {', '.join(c.display_name + f'({c.hp}/{c.max_hp})' for c in self.bot.creatures)}"""

    def run(self):
        while True:
            # Show current state
            self._show_text(self.player, str(self))
            
            # Get actions
            p_action = self.get_turn_action(self.player)
            b_action = self.get_turn_action(self.bot)
            
            # Execute actions
            self.resolve_turn(p_action, b_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_turn_action(self, player: Player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skills = [SelectThing(s) for s in player.active_creature.skills]
            back_button = Button("Back")
            skill_choice = self._wait_for_choice(player, skills + [back_button])
            
            if skill_choice == back_button:
                return self.get_turn_action(player)
            return ("attack", skill_choice.thing)
            
        else:
            # Show available creatures
            available = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
            creatures = [SelectThing(c) for c in available]
            back_button = Button("Back")
            
            if not creatures:
                return self.get_turn_action(player)
                
            swap_choice = self._wait_for_choice(player, creatures + [back_button])
            
            if swap_choice == back_button:
                return self.get_turn_action(player)
            return ("swap", swap_choice.thing)

    def resolve_turn(self, p_action, b_action):
        # Handle swaps first
        if p_action[0] == "swap":
            self.player.active_creature = p_action[1]
        if b_action[0] == "swap":
            self.bot.active_creature = b_action[1]
            
        # Skip attacks if creature is knocked out
        if self.player.active_creature.hp <= 0 or self.bot.active_creature.hp <= 0:
            return
            
        # Determine attack order
        first = self.player
        second = self.bot
        first_action = p_action
        second_action = b_action
        
        if (b_action[0] == "attack" and p_action[0] == "attack" and
            (self.bot.active_creature.speed > self.player.active_creature.speed or 
             (self.bot.active_creature.speed == self.player.active_creature.speed and 
              random.random() < 0.5))):
            first = self.bot
            second = self.player
            first_action = b_action
            second_action = p_action
            
        # Execute attacks
        if first_action[0] == "attack":
            self.execute_attack(first, second, first_action[1])
        if second_action[0] == "attack" and second.active_creature.hp > 0:
            self.execute_attack(second, first, second_action[1])
            
        # Force swaps for knocked out creatures
        for p in [self.player, self.bot]:
            if p.active_creature.hp <= 0:
                available = [c for c in p.creatures if c.hp > 0]
                if available:
                    choices = [SelectThing(c) for c in available]
                    swap_choice = self._wait_for_choice(p, choices)
                    p.active_creature = swap_choice.thing

    def execute_attack(self, attacker: Player, defender: Player, skill):
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
        
        # Show result
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {final_damage} damage!")

    def get_type_effectiveness(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def check_battle_end(self) -> bool:
        p_alive = any(c.hp > 0 for c in self.player.creatures)
        b_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_alive or not b_alive:
            winner = self.player if p_alive else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
