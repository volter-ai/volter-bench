from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.reset_creatures()

    def reset_creatures(self):
        # Reset all creatures to max HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
{"> Swap" if self.has_valid_swaps(self.player) else ""}
"""

    def has_valid_swaps(self, player):
        return any(c for c in player.creatures if c.hp > 0 and c != player.active_creature)

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Properly end the game instead of just breaking
                self._quit_whole_game()

    def get_player_action(self, player):
        # Always show Attack button
        choices = [Button("Attack")]
        
        # Only show Swap if there are valid creatures to swap to
        if self.has_valid_swaps(player):
            choices.append(Button("Swap"))
        
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            return self._wait_for_choice(player, skill_choices)
        else:
            # Show available creatures
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            return self._wait_for_choice(player, creature_choices)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
            self._show_text(self.player, f"You switched to {player_action.thing.display_name}!")
            
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            self._show_text(self.player, f"Foe switched to {bot_action.thing.display_name}!")

        # Then handle attacks
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Sort by speed for attack order
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        for attacker, action in actions:
            if isinstance(action.thing, Creature):
                continue
                
            defender = self.bot if attacker == self.player else self.player
            self.execute_attack(attacker, defender, action.thing)
            
            # Force swap if creature fainted
            if defender.active_creature.hp <= 0:
                available_creatures = [c for c in defender.creatures if c.hp > 0]
                if available_creatures:
                    new_creature = random.choice(available_creatures)
                    defender.active_creature = new_creature
                    self._show_text(self.player, f"{'Foe' if defender == self.bot else 'You'} switched to {new_creature.display_name}!")

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show message
        self._show_text(self.player, 
            f'{"Your" if attacker == self.player else "Foe"} {attacker.active_creature.display_name} used {skill.display_name}!')

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures or not bot_has_creatures:
            winner = "You win!" if bot_has_creatures else "You lose!"
            self._show_text(self.player, winner)
            return True
            
        return False
