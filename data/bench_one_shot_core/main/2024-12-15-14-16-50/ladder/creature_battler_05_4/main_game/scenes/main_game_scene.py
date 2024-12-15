from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.reset_creatures()

    def reset_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        while True:
            player_action = self.get_player_action(self.player)
            if not player_action:
                return
                
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                return
                
            self.resolve_turn(player_action, bot_action)
            
            if self.check_battle_end():
                return

    def get_player_action(self, current_player):
        while True:
            choice = self._wait_for_choice(current_player, [
                Button("Attack"),
                Button("Swap")
            ])

            if choice.display_name == "Attack":
                skills = [SelectThing(skill) for skill in current_player.active_creature.skills]
                skills.append(Button("Back"))
                skill_choice = self._wait_for_choice(current_player, skills)
                
                if isinstance(skill_choice, Button):
                    continue
                    
                return ("attack", skill_choice.thing)
                
            else:
                available_creatures = [
                    SelectThing(c) for c in current_player.creatures 
                    if c != current_player.active_creature and c.hp > 0
                ]
                if not available_creatures:
                    self._show_text(current_player, "No creatures available to swap!")
                    continue
                    
                available_creatures.append(Button("Back"))
                creature_choice = self._wait_for_choice(current_player, available_creatures)
                
                if isinstance(creature_choice, Button):
                    continue
                    
                return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"You swapped to {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Foe swapped to {bot_action[1].display_name}!")

        # Create action tuples with (action_type, action_data, attacker, target)
        player_full_action = (
            player_action[0],
            player_action[1],
            self.player,
            self.bot.active_creature
        )
        bot_full_action = (
            bot_action[0],
            bot_action[1],
            self.bot,
            self.player.active_creature
        )

        # Get action order and execute
        first, second = self.get_action_order(player_full_action, bot_full_action)
        self.execute_action(first)
        
        # Only execute second action if target is still alive
        if second[3].hp > 0:  # Check target's HP
            self.execute_action(second)

    def get_action_order(self, player_full_action, bot_full_action):
        # Swaps always go first
        if player_full_action[0] == "swap" or bot_full_action[0] == "swap":
            return (player_full_action, bot_full_action) if player_full_action[0] == "swap" else (bot_full_action, player_full_action)
            
        player_speed = self.player.active_creature.speed
        bot_speed = self.bot.active_creature.speed
        
        if player_speed > bot_speed:
            return (player_full_action, bot_full_action)
        elif bot_speed > player_speed:
            return (bot_full_action, player_full_action)
        else:
            return random.choice([(player_full_action, bot_full_action), (bot_full_action, player_full_action)])

    def execute_action(self, action):
        action_type, action_data, attacker, target = action
        
        if action_type != "attack":
            return
            
        skill = action_data
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - target.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / target.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, target.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        target.hp = max(0, target.hp - final_damage)
        
        # Show message
        self._show_text(self.player, 
            f"{'You' if attacker == self.player else 'Foe'} used {skill.display_name}! "
            f"It dealt {final_damage} damage!")
            
        # Handle fainting
        if target.hp <= 0:
            self._show_text(self.player,
                f"{'Foe' if attacker == self.player else 'Your'} {target.display_name} fainted!")
            self.handle_faint(self.bot if attacker == self.player else self.player)

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def handle_faint(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        self._show_text(player, "Choose a new creature!")
        choice = self._wait_for_choice(player, [SelectThing(c) for c in available_creatures])
        player.active_creature = choice.thing

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            self._show_text(self.player, "You win!" if player_alive else "You lose!")
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
