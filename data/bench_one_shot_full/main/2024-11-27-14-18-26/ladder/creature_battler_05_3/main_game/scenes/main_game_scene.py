from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

    def __str__(self):
        p1 = self.player
        p2 = self.bot
        
        return f"""=== Battle ===
{p1.display_name}'s {p1.active_creature.display_name}: {p1.active_creature.hp}/{p1.active_creature.max_hp} HP
{p2.display_name}'s {p2.active_creature.display_name}: {p2.active_creature.hp}/{p2.active_creature.max_hp} HP

> Attack
> Swap (if available)
"""

    def run(self):
        while True:
            # Check for battle end before each turn
            if self.check_battle_end():
                break
                
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)

        # Reset creatures
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = None

        self._transition_to_scene("MainMenuScene")

    def get_valid_swap_creatures(self, player):
        return [c for c in player.creatures if c != player.active_creature and c.hp > 0]

    def get_player_action(self, player):
        choices = []
        
        # Always add Attack option if creature is alive
        if player.active_creature.hp > 0:
            choices.append(Button("Attack"))
            
        # Only add Swap option if there are valid creatures to swap to
        valid_swap_creatures = self.get_valid_swap_creatures(player)
        if valid_swap_creatures:
            choices.append(Button("Swap"))
            
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            choices = [SelectThing(skill) for skill in player.active_creature.skills]
            return self._wait_for_choice(player, choices)
        else:  # Swap
            choices = [SelectThing(c) for c in valid_swap_creatures]
            return self._wait_for_choice(player, choices)

    def resolve_turn(self, p1_action, p2_action):
        # Handle swaps first
        for action, player in [(p1_action, self.player), (p2_action, self.bot)]:
            if isinstance(action.thing, Creature):
                player.active_creature = action.thing
                self._show_text(player, f"{player.display_name} swapped to {action.thing.display_name}!")

        # Then handle attacks
        actions = [(p1_action, self.player, self.bot), (p2_action, self.bot, self.player)]
        actions.sort(key=lambda x: x[1].active_creature.speed, reverse=True)
        
        for action, attacker, defender in actions:
            if isinstance(action.thing, Creature):
                continue
                
            skill = action.thing
            damage = self.calculate_damage(skill, attacker.active_creature, defender.active_creature)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            
            self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
            self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")
            
            if defender.active_creature.hp == 0:
                self._show_text(defender, f"{defender.active_creature.display_name} was knocked out!")
                valid_creatures = self.get_valid_swap_creatures(defender)
                if valid_creatures:
                    choices = [SelectThing(c) for c in valid_creatures]
                    swap = self._wait_for_choice(defender, choices)
                    defender.active_creature = swap.thing
                    self._show_text(defender, f"{defender.display_name} sent out {swap.thing.display_name}!")

    def calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        for player in [self.player, self.bot]:
            if all(c.hp == 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                return True
                
            # Also check if active creature is knocked out and no valid swaps
            if player.active_creature.hp == 0 and not self.get_valid_swap_creatures(player):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                return True
                
        return False
