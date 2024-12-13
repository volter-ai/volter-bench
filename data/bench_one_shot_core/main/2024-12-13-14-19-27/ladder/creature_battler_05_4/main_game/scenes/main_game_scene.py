from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
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

    def is_creature_knocked_out(self, creature: Creature) -> bool:
        return creature.hp <= 0

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
                self._quit_whole_game()

    def get_player_action(self, player):
        while True:
            choice = self._wait_for_choice(player, [
                Button("Attack"),
                Button("Swap")
            ])
            
            if choice.display_name == "Attack":
                skills = [SelectThing(skill) for skill in player.active_creature.skills]
                skills.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skills)
                
                if isinstance(skill_choice, SelectThing):
                    return ("attack", skill_choice.thing)
                    
            else: # Swap
                available_creatures = [
                    SelectThing(c) for c in player.creatures 
                    if c != player.active_creature and not self.is_creature_knocked_out(c)
                ]
                available_creatures.append(Button("Back"))
                
                if not available_creatures:
                    self._show_text(player, "No creatures available to swap!")
                    continue
                    
                creature_choice = self._wait_for_choice(player, available_creatures)
                
                if isinstance(creature_choice, SelectThing):
                    return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            
        # Then handle attacks
        first_action, second_action = self.get_action_order(player_action, bot_action)
        self.execute_action(first_action[0], first_action[1])
        
        if not self.check_battle_end():
            self.execute_action(second_action[0], second_action[1])

    def get_action_order(self, player_action, bot_action):
        if player_action[0] == "swap" or bot_action[0] == "swap":
            return (player_action, bot_action)
            
        player_speed = self.player.active_creature.speed
        bot_speed = self.bot.active_creature.speed
        
        if player_speed > bot_speed:
            return (player_action, bot_action)
        elif bot_speed > player_speed:
            return (bot_action, player_action)
        else:
            if random.random() < 0.5:
                return (player_action, bot_action)
            return (bot_action, player_action)

    def execute_action(self, action_type, action_data):
        if action_type == "attack":
            attacker = self.player if action_data in self.player.active_creature.skills else self.bot
            defender = self.bot if attacker == self.player else self.player
            
            damage = self.calculate_damage(
                attacker.active_creature,
                defender.active_creature,
                action_data
            )
            
            defender.active_creature.hp -= damage
            self._show_text(self.player, 
                f"{attacker.active_creature.display_name} used {action_data.display_name}! "
                f"Dealt {damage} damage!")

    def calculate_damage(self, attacker: Creature, defender: Creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        def has_available_creatures(player):
            return any(not self.is_creature_knocked_out(c) for c in player.creatures)
            
        if self.is_creature_knocked_out(self.player.active_creature):
            if has_available_creatures(self.player):
                available = [SelectThing(c) for c in self.player.creatures 
                           if not self.is_creature_knocked_out(c)]
                choice = self._wait_for_choice(self.player, available)
                if isinstance(choice, SelectThing):
                    self.player.active_creature = choice.thing
                return False
            else:
                self._show_text(self.player, "You lost the battle!")
                return True
                
        if self.is_creature_knocked_out(self.bot.active_creature):
            if has_available_creatures(self.bot):
                available = [c for c in self.bot.creatures 
                           if not self.is_creature_knocked_out(c)]
                self.bot.active_creature = random.choice(available)
                return False
            else:
                self._show_text(self.player, "You won the battle!")
                return True
                
        return False
