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
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

> Attack
> Swap (if you have other creatures available)"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break
                
        # Reset creatures
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = None
            
        self._transition_to_scene("MainMenuScene")

    def get_player_action(self, player):
        while True:
            # Check if there are creatures available to swap to
            available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
            
            # Build choice list based on available options
            choices = [Button("Attack")]
            if available_creatures:
                choices.append(Button("Swap"))
            
            main_choice = self._wait_for_choice(player, choices)
            
            if main_choice.display_name == "Attack":
                # Show skills with back option
                action_choices = [SelectThing(s) for s in player.active_creature.skills]
                back_choice = self._wait_for_choice(player, [Button("Back")] + action_choices)
                
                if isinstance(back_choice, Button):
                    continue  # Go back to main choices
                return back_choice
            else:
                # Show creatures with back option
                action_choices = [SelectThing(c) for c in available_creatures]
                back_choice = self._wait_for_choice(player, [Button("Back")] + action_choices)
                
                if isinstance(back_choice, Button):
                    continue  # Go back to main choices
                return back_choice

    def resolve_turn(self, p_action, b_action):
        # Handle swaps first
        if isinstance(p_action.thing, Creature):
            self.player.active_creature = p_action.thing
        if isinstance(b_action.thing, Creature):
            self.bot.active_creature = b_action.thing
            
        # Then handle attacks
        actions = [(self.player, p_action), (self.bot, b_action)]
        
        # Sort by speed, handling ties randomly
        def get_speed_key(action_tuple):
            player, action = action_tuple
            return (player.active_creature.speed, random.random())
            
        actions.sort(key=get_speed_key, reverse=True)
        
        for player, action in actions:
            if isinstance(action.thing, Creature):
                continue
                
            skill = action.thing
            target = self.bot if player == self.player else self.player
            
            damage = self.calculate_damage(skill, player.active_creature, target.active_creature)
            target.active_creature.hp = max(0, target.active_creature.hp - damage)
            
            self._show_text(player, f"{player.active_creature.display_name} used {skill.display_name}!")
            self._show_text(player, f"Dealt {damage} damage!")
            
            if target.active_creature.hp == 0:
                self.handle_knockout(target)

    def calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw = attacker.attack + skill.base_damage - defender.defense
        else:
            raw = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw * effectiveness)

    def get_type_effectiveness(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def handle_knockout(self, player):
        available = [c for c in player.creatures if c.hp > 0]
        if not available:
            winner = self.player if player == self.bot else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            return
            
        creatures = [SelectThing(c) for c in available]
        new_creature = self._wait_for_choice(player, creatures).thing
        player.active_creature = new_creature

    def check_battle_end(self):
        for p in [self.player, self.bot]:
            if all(c.hp == 0 for c in p.creatures):
                return True
        return False
