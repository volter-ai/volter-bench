from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, AbstractPlayer
from main_game.models import Creature
import random
from typing import Tuple, List

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.bot.display_name}'s {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap (if you have other creatures available)"""

    def run(self):
        while True:
            # Player turn - now returns tuple of (action, player)
            player_action = (self.get_player_action(self.player), self.player)
            bot_action = (self.get_player_action(self.bot), self.bot)
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_valid_swap_creatures(self, player: AbstractPlayer) -> List[Creature]:
        """Get list of creatures that can be swapped to"""
        return [c for c in player.creatures 
                if c.hp > 0 and c != player.active_creature]

    def get_player_action(self, player: AbstractPlayer):
        # Always offer attack
        choices = [Button("Attack")]
        
        # Only offer swap if there are valid creatures to swap to
        valid_swap_creatures = self.get_valid_swap_creatures(player)
        if valid_swap_creatures:
            choices.append(Button("Swap"))
        
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            choices = [SelectThing(skill) for skill in player.active_creature.skills]
            return self._wait_for_choice(player, choices)
        else:
            choices = [SelectThing(creature) for creature in valid_swap_creatures]
            return self._wait_for_choice(player, choices)

    def resolve_turn(self, player_action: Tuple[SelectThing, AbstractPlayer], 
                    bot_action: Tuple[SelectThing, AbstractPlayer]):
        # Handle swaps first
        if isinstance(player_action[0].thing, Creature):
            self.player.active_creature = player_action[0].thing
        if isinstance(bot_action[0].thing, Creature):
            self.bot.active_creature = bot_action[0].thing
            
        # Then handle attacks
        first, second = self.get_action_order(player_action, bot_action)
        self.execute_action(first[0], first[1])  # Pass both action and player
        self.execute_action(second[0], second[1])

    def get_action_order(self, player_action: Tuple[SelectThing, AbstractPlayer], 
                        bot_action: Tuple[SelectThing, AbstractPlayer]):
        player_speed = self.player.active_creature.speed
        bot_speed = self.bot.active_creature.speed
        
        if player_speed > bot_speed:
            return player_action, bot_action
        elif bot_speed > player_speed:
            return bot_action, player_action
        else:
            if random.random() < 0.5:
                return player_action, bot_action
            return bot_action, player_action

    def execute_action(self, action: SelectThing, acting_player: AbstractPlayer):
        if isinstance(action.thing, Creature):
            return
            
        skill = action.thing
        attacker = acting_player.active_creature
        defender = self.bot.active_creature if acting_player == self.player else self.player.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.hp = max(0, defender.hp - final_damage)
        
        # Force swap if knocked out
        if defender.hp <= 0:
            self.handle_knockout(defender)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, knocked_out_creature):
        player = self.player if knocked_out_creature in self.player.creatures else self.bot
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        
        if valid_creatures:
            choices = [SelectThing(creature) for creature in valid_creatures]
            new_creature = self._wait_for_choice(player, choices).thing
            player.active_creature = new_creature

    def check_battle_end(self):
        player_has_valid = any(c.hp > 0 for c in self.player.creatures)
        bot_has_valid = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_valid:
            self._show_text(self.player, "You lost!")
            return True
        elif not bot_has_valid:
            self._show_text(self.player, "You won!")
            return True
            
        return False
