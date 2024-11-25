from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, create_from_game_database
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
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
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._transition_to_scene("MainMenuScene")  # Return to menu after battle ends

    def get_player_action(self, player):
        if player.active_creature.hp <= 0:
            if not self.handle_fainted_creature(player):
                return None
                
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
            return self.get_player_action(player)
            
        return {"type": "attack", "skill": choice.thing, "creature": player.active_creature}

    def handle_swap_choice(self, player):
        available_creatures = [
            creature for creature in player.creatures 
            if creature.hp > 0 and creature != player.active_creature
        ]
        
        if not available_creatures:
            self._show_text(player, "No other creatures available!")
            return self.get_player_action(player)
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, creature_choices + [back_button])
        
        if choice == back_button:
            return self.get_player_action(player)
            
        return {"type": "swap", "creature": choice.thing}

    def handle_fainted_creature(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if not available_creatures:
            return False
            
        self._show_text(player, f"{player.active_creature.display_name} has fainted! Choose a new creature!")
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        return True

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"Go, {player_action['creature'].display_name}!")
            
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            self._show_text(self.player, f"Foe sends out {bot_action['creature'].display_name}!")
            
        # Then handle attacks
        if player_action["type"] == "attack" and bot_action["type"] == "attack":
            first, second = self.determine_turn_order(player_action, bot_action)
            self.execute_attack(first)
            if second["creature"].hp > 0:  # Only do second attack if target still alive
                self.execute_attack(second)

    def determine_turn_order(self, action1, action2):
        if action1["creature"].speed > action2["creature"].speed:
            return action1, action2
        elif action2["creature"].speed > action1["creature"].speed:
            return action2, action1
        else:
            return random.choice([(action1, action2), (action2, action1)])

    def execute_attack(self, action):
        attacker = action["creature"]
        defender = self.bot.active_creature if attacker == self.player.active_creature else self.player.active_creature
        skill = action["skill"]
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.hp = max(0, defender.hp - final_damage)
        
        # Show message
        effectiveness = "It's super effective!" if multiplier > 1 else "It's not very effective..." if multiplier < 1 else ""
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! {effectiveness}")

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You have been defeated!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You are victorious!")
            return True
            
        return False
