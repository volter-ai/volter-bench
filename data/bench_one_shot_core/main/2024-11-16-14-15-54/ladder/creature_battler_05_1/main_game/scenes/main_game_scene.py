from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Skill, Creature
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
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Enemy {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap (if you have other conscious creatures)"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()  # Signal game end properly instead of just breaking
            
            # Handle forced swaps for fainted creatures
            if self.player.active_creature.hp <= 0:
                self.handle_forced_swap(self.player)
            if self.bot.active_creature.hp <= 0:
                self.handle_forced_swap(self.bot)

    def get_valid_swap_targets(self, player):
        return [c for c in player.creatures 
                if c != player.active_creature and c.hp > 0]

    def get_player_action(self, player):
        choices = [Button("Attack")]
        
        # Only add swap option if there are valid targets
        valid_swap_targets = self.get_valid_swap_targets(player)
        if valid_swap_targets:
            choices.append(Button("Swap"))
        
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            return self._wait_for_choice(player, 
                [SelectThing(skill) for skill in player.active_creature.skills])
        else:
            return self._wait_for_choice(player,
                [SelectThing(creature) for creature in valid_swap_targets])

    def handle_forced_swap(self, player):
        valid_creatures = self.get_valid_swap_targets(player)
        if valid_creatures:
            swap_choice = self._wait_for_choice(player,
                [SelectThing(creature) for creature in valid_creatures])
            player.active_creature = swap_choice.thing
            self._show_text(player, f"Swapped to {swap_choice.thing.display_name}!")
        else:
            # If no valid swaps, this will trigger battle end check next loop
            pass

    def resolve_turn(self, player_action, bot_action):
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Swaps go first
        actions.sort(key=lambda x: isinstance(x[1].thing, Skill))
        
        for player, action in actions:
            if isinstance(action.thing, Skill):
                self.execute_skill(player, action.thing)
            else:
                player.active_creature = action.thing
                self._show_text(player, f"Swapped to {action.thing.display_name}!")

    def execute_skill(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        
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
        
        final_damage = max(1, int(raw_damage * multiplier))  # Minimum 1 damage
        defender.active_creature.hp -= final_damage
        
        self._show_text(attacker, 
            f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender,
            f"{defender.active_creature.display_name} took {final_damage} damage!")

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
        def has_conscious_creatures(player):
            return any(c.hp > 0 for c in player.creatures)
            
        if not has_conscious_creatures(self.player):
            self._show_text(self.player, "You lost!")
            return True
        elif not has_conscious_creatures(self.bot):
            self._show_text(self.player, "You won!")
            return True
            
        return False
