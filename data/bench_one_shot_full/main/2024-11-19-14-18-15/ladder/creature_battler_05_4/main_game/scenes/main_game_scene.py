from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
from typing import Dict, List
from copy import deepcopy

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Store initial creature states
        self.initial_player_creatures = deepcopy(self.player.creatures)
        self.initial_bot_creatures = deepcopy(self.bot.creatures)
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

> Attack
> Swap"""

    def reset_creature_states(self):
        """Restore all creatures to their initial states"""
        for i, creature in enumerate(self.initial_player_creatures):
            self.player.creatures[i].hp = creature.hp
            self.player.creatures[i].max_hp = creature.max_hp
            
        for i, creature in enumerate(self.initial_bot_creatures):
            self.bot.creatures[i].hp = creature.hp
            self.bot.creatures[i].max_hp = creature.max_hp
        
        self.player.active_creature = None
        self.bot.active_creature = None

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                continue
                
            # Resolve actions
            if not self.resolve_turn(player_action, bot_action):
                self.reset_creature_states()
                self._quit_whole_game()

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self.handle_attack_choice(player)
        else:
            return self.handle_swap_choice(player)

    def handle_attack_choice(self, player):
        skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, skill_choices + [back_button])
        
        if choice == back_button:
            return None
        return {"type": "attack", "skill": choice.thing}

    def handle_swap_choice(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        if not available_creatures:
            self._show_text(player, "No other creatures available!")
            return None
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, creature_choices + [back_button])
        
        if choice == back_button:
            return None
        return {"type": "swap", "creature": choice.thing}

    def force_swap_knocked_out(self, player):
        """Force player to swap when active creature is knocked out"""
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return False
            
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        self._show_text(player, f"Sent out {player.active_creature.display_name}!")
        return True

    def resolve_turn(self, player_action, bot_action):
        """Returns False if battle should end, True if it should continue"""
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            
        # Then handle attacks
        if player_action["type"] == "attack" and bot_action["type"] == "attack":
            first, second = self.determine_order(self.player, self.bot)
            
            # First attack
            self.execute_attack(first, second)
            if second.active_creature.hp <= 0:
                if not self.force_swap_knocked_out(second):
                    self._show_text(first, f"{second.display_name} has no more creatures!")
                    return False
            
            # Second attack (only if creature still conscious)
            if second.active_creature.hp > 0:
                self.execute_attack(second, first)
                if first.active_creature.hp <= 0:
                    if not self.force_swap_knocked_out(first):
                        self._show_text(second, f"{first.display_name} has no more creatures!")
                        return False
        
        return True

    def determine_order(self, player1, player2):
        speed1 = player1.active_creature.speed
        speed2 = player2.active_creature.speed
        
        if speed1 > speed2:
            return player1, player2
        elif speed2 > speed1:
            return player2, player1
        else:
            return random.choice([(player1, player2), (player2, player1)])

    def execute_attack(self, attacker, defender):
        skill = attacker.active_creature.skills[0]  # For simplicity
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"Dealt {damage} damage!")

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        type_factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * type_factor)

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
