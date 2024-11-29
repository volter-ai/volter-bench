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

Your other creatures: {[c.display_name for c in self.player.creatures if c != p_creature and c.hp > 0]}
Foe's other creatures: {[c.display_name for c in self.bot.creatures if c != b_creature and c.hp > 0]}"""

    def reset_creatures(self):
        """Reset all creatures to their initial state"""
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self.reset_creatures()  # Reset before quitting
                self._quit_whole_game()

    def get_player_action(self, player):
        if player.active_creature.hp <= 0:
            return self.force_swap(player)
            
        attack = Button("Attack")
        swap = Button("Swap")
        choice = self._wait_for_choice(player, [attack, swap])
        
        if choice == attack:
            return self.choose_attack(player)
        else:
            return self.choose_swap(player)

    def choose_attack(self, player):
        skills = [SelectThing(s) for s in player.active_creature.skills]
        back = Button("Back")
        choice = self._wait_for_choice(player, skills + [back])
        
        if choice == back:
            return self.get_player_action(player)
        return {"type": "attack", "skill": choice.thing}

    def choose_swap(self, player):
        available = [SelectThing(c) for c in player.creatures 
                    if c != player.active_creature and c.hp > 0]
        back = Button("Back")
        choice = self._wait_for_choice(player, available + [back])
        
        if choice == back:
            return self.get_player_action(player)
        return {"type": "swap", "creature": choice.thing}

    def force_swap(self, player):
        available = [SelectThing(c) for c in player.creatures if c.hp > 0]
        if not available:
            return None
        choice = self._wait_for_choice(player, available)
        return {"type": "swap", "creature": choice.thing}

    def resolve_turn(self, p_action, b_action):
        if not p_action or not b_action:
            return
            
        # Handle swaps first
        if p_action["type"] == "swap":
            self.player.active_creature = p_action["creature"]
        if b_action["type"] == "swap":
            self.bot.active_creature = b_action["creature"]
            
        # Then handle attacks
        if p_action["type"] == "attack" and b_action["type"] == "attack":
            first, second = self.determine_order(
                (self.player, p_action), 
                (self.bot, b_action)
            )
            self.execute_attack(*first)
            if second[1]["type"] == "attack":  # Only if target still alive
                self.execute_attack(*second)

    def determine_order(self, p_pair, b_pair):
        p_speed = p_pair[0].active_creature.speed
        b_speed = b_pair[0].active_creature.speed
        
        if p_speed > b_speed:
            return p_pair, b_pair
        elif b_speed > p_speed:
            return b_pair, p_pair
        else:
            return random.choice([(p_pair, b_pair), (b_pair, p_pair)])

    def execute_attack(self, attacker, action):
        if attacker == self.player:
            defender = self.bot
        else:
            defender = self.player
            
        skill = action["skill"]
        target = defender.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         target.defense)
        else:
            raw_damage = ((attacker.active_creature.sp_attack / 
                          target.sp_defense) * 
                         skill.base_damage)
            
        # Apply type effectiveness
        factor = self.get_type_factor(skill.skill_type, target.creature_type)
        final_damage = int(raw_damage * factor)
        
        target.hp = max(0, target.hp - final_damage)
        self._show_text(attacker, 
            f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender,
            f"{target.display_name} took {final_damage} damage!")

    def get_type_factor(self, skill_type, target_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(target_type, 1.0)

    def check_battle_end(self):
        p_alive = any(c.hp > 0 for c in self.player.creatures)
        b_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_alive or not b_alive:
            self._show_text(self.player, 
                "You win!" if p_alive else "You lose!")
            return True
        return False
