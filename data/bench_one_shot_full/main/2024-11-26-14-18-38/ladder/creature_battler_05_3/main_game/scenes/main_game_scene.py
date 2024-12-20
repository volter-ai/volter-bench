from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
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

Your other creatures: {[c.display_name for c in self.player.creatures if c != p_creature and c.hp > 0]}
Foe's other creatures: {[c.display_name for c in self.bot.creatures if c != b_creature and c.hp > 0]}
"""

    def run(self):
        while True:
            # Show current state
            self._show_text(self.player, str(self))
            
            # Get player action
            player_action = self.get_player_action(self.player)
            if not player_action:
                return
                
            # Get bot action
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                return
                
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._reset_creatures()  # Reset creatures before leaving scene
                self._quit_whole_game()
                return

    def _reset_creatures(self):
        """Reset all creatures to their initial state before leaving the scene"""
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

    def get_player_action(self, player):
        # Force swap if active creature is knocked out
        if player.active_creature.hp <= 0:
            available = [c for c in player.creatures if c.hp > 0]
            if not available:
                return None
            
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            return {"type": "swap", "creature": choice.thing}

        # Normal turn choices
        while True:
            choice = self._wait_for_choice(player, [
                Button("Attack"),
                Button("Swap"),
            ])

            if choice.display_name == "Attack":
                skill_choices = [SelectThing(s) for s in player.active_creature.skills]
                skill_choice = self._wait_for_choice(player, skill_choices + [Button("Back")])
                if isinstance(skill_choice, Button):
                    continue
                return {"type": "attack", "skill": skill_choice.thing}
            
            else: # Swap
                available = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                if not available:
                    continue
                    
                swap_choices = [SelectThing(c) for c in available]
                swap_choice = self._wait_for_choice(player, swap_choices + [Button("Back")])
                if isinstance(swap_choice, Button):
                    continue
                return {"type": "swap", "creature": swap_choice.thing}

    def resolve_actions(self, p_action, b_action):
        # Handle swaps first
        if p_action["type"] == "swap":
            self.player.active_creature = p_action["creature"]
        if b_action["type"] == "swap":
            self.bot.active_creature = b_action["creature"]

        # Then handle attacks
        if p_action["type"] == "attack" and b_action["type"] == "attack":
            # Determine order
            first = self.player
            second = self.bot
            first_action = p_action
            second_action = b_action
            
            if self.bot.active_creature.speed > self.player.active_creature.speed or \
               (self.bot.active_creature.speed == self.player.active_creature.speed and random.random() < 0.5):
                first = self.bot
                second = self.player
                first_action = b_action
                second_action = p_action

            # Execute attacks
            self.execute_attack(first, second, first_action["skill"])
            if second.active_creature.hp > 0:
                self.execute_attack(second, first, second_action["skill"])

        elif p_action["type"] == "attack":
            self.execute_attack(self.player, self.bot, p_action["skill"])
        elif b_action["type"] == "attack":
            self.execute_attack(self.bot, self.player, b_action["skill"])

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        factor = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * factor)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show result
        effectiveness = "It's super effective!" if factor > 1 else "It's not very effective..." if factor < 1 else ""
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! {effectiveness}\n"
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}!")

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def check_battle_end(self):
        p_alive = any(c.hp > 0 for c in self.player.creatures)
        b_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_alive or not b_alive:
            self._show_text(self.player, "You win!" if p_alive else "You lose!")
            return True
            
        return False
