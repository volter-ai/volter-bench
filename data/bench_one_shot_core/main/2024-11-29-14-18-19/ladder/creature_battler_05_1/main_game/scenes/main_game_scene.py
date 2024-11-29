from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Player
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures and reset their HP
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Reset all creatures to max HP at start
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue
                
            # Bot turn
            bot_action = self.get_bot_action()
            if not bot_action:
                continue
            
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Reset creatures before ending
                for creature in self.player.creatures:
                    creature.hp = creature.max_hp
                for creature in self.bot.creatures:
                    creature.hp = creature.max_hp
                break

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self.handle_attack_choice(player)
        else:
            return self.handle_swap_choice(player)

    def get_bot_action(self):
        try:
            if len([c for c in self.bot.creatures if c.hp > 0]) > 1:
                action = self._wait_for_choice(self.bot, [Button("Attack"), Button("Swap")])
                if action.display_name == "Attack":
                    return self.handle_attack_choice(self.bot)
                else:
                    return self.handle_swap_choice(self.bot)
            else:
                return self.handle_attack_choice(self.bot)
        except Exception:
            return self.handle_attack_choice(self.bot)

    def handle_attack_choice(self, player):
        creature = player.active_creature
        choices = [SelectThing(skill) for skill in creature.skills]
        choices.append(Button("Back"))
        
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button):
            return None
            
        return {"type": "attack", "skill": choice.thing}

    def handle_swap_choice(self, player):
        available_creatures = [c for c in player.creatures 
                             if c != player.active_creature and c.hp > 0]
        
        if not available_creatures:
            self._show_text(player, "No creatures available to swap!")
            return None
            
        choices = [SelectThing(c) for c in available_creatures]
        choices.append(Button("Back"))
        
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button):
            return None
            
        return {"type": "swap", "creature": choice.thing}

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action and player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"Go {player_action['creature'].display_name}!")
            
        if bot_action and bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            self._show_text(self.player, f"Foe sends out {bot_action['creature'].display_name}!")

        # Then handle attacks
        if (player_action and bot_action and 
            player_action["type"] == "attack" and bot_action["type"] == "attack"):
            
            player_speed = self.player.active_creature.speed
            bot_speed = self.bot.active_creature.speed
            
            # Determine order based on speed with random tie-breaking
            if player_speed > bot_speed:
                first, second = (self.player, player_action), (self.bot, bot_action)
            elif bot_speed > player_speed:
                first, second = (self.bot, bot_action), (self.player, player_action)
            else:
                # Equal speeds - randomly determine order
                if random.random() < 0.5:
                    first, second = (self.player, player_action), (self.bot, bot_action)
                else:
                    first, second = (self.bot, bot_action), (self.player, player_action)
            
            # Execute attacks in determined order
            self.execute_attack(first[0], second[0], first[1]["skill"])
            if second[0].active_creature.hp > 0:  # Only execute second attack if target still alive
                self.execute_attack(second[0], first[0], second[1]["skill"])

    def execute_attack(self, attacker, defender, skill):
        if defender.active_creature.hp <= 0:
            return
            
        # Calculate damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         defender.active_creature.defense)
        else:
            raw_damage = (skill.base_damage * 
                         attacker.active_creature.sp_attack / 
                         defender.active_creature.sp_defense)
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, 
                                            defender.active_creature.creature_type)
        
        final_damage = max(1, int(raw_damage * multiplier))
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
                       f"{attacker.active_creature.display_name} used {skill.display_name}!")
        
        if multiplier > 1:
            self._show_text(self.player, "It's super effective!")
        elif multiplier < 1:
            self._show_text(self.player, "It's not very effective...")

    def get_type_multiplier(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def check_battle_end(self):
        def has_available_creatures(player):
            return any(c.hp > 0 for c in player.creatures)
            
        if not has_available_creatures(self.player):
            self._show_text(self.player, "You lost the battle!")
            return True
            
        if not has_available_creatures(self.bot):
            self._show_text(self.player, "You won the battle!")
            return True
            
        if (self.player.active_creature.hp <= 0 and 
            has_available_creatures(self.player)):
            self.force_swap(self.player)
            
        if (self.bot.active_creature.hp <= 0 and 
            has_available_creatures(self.bot)):
            self.force_swap(self.bot)
            
        return False

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        choices = [SelectThing(c) for c in available_creatures]
        
        self._show_text(player, f"{player.active_creature.display_name} fainted!")
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        self._show_text(player, f"Go {choice.thing.display_name}!")
