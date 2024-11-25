from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        # Initialize creatures for both players
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

Main Menu:
> Attack
> Swap (if you have available creatures)

When in Attack or Swap menu:
> [Options...]
> Back
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

        # Reset creatures
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = None

        self._transition_to_scene("MainMenuScene")

    def get_available_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def get_player_action(self, player):
        while True:
            # Build main menu choices
            choices = [Button("Attack")]
            available_creatures = self.get_available_creatures(player)
            if available_creatures:
                choices.append(Button("Swap"))
                
            main_choice = self._wait_for_choice(player, choices)
            
            if main_choice.display_name == "Attack":
                # Show skills with Back option
                skill_choices = [SelectThing(s) for s in player.active_creature.skills]
                back_button = Button("Back")
                skill_choices.append(back_button)
                
                choice = self._wait_for_choice(player, skill_choices)
                if choice == back_button:
                    continue  # Go back to main menu
                return choice
            else:
                # Show available creatures with Back option
                creature_choices = [SelectThing(c) for c in available_creatures]
                back_button = Button("Back")
                creature_choices.append(back_button)
                
                choice = self._wait_for_choice(player, creature_choices)
                if choice == back_button:
                    continue  # Go back to main menu
                return choice

    def resolve_actions(self, player_action, bot_action):
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Handle swaps first
        for player, action in actions:
            if isinstance(action.thing, Creature):
                player.active_creature = action.thing
                self._show_text(player, f"{player.display_name} swapped to {action.thing.display_name}!")

        # Then handle attacks
        # Sort by speed
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        for player, action in actions:
            if hasattr(action.thing, 'skill_type'):  # Is a skill
                self.execute_skill(player, action.thing)

    def execute_skill(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        
        if multiplier > 1:
            self._show_text(attacker, "It's super effective!")
        elif multiplier < 1:
            self._show_text(attacker, "It's not very effective...")

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1
        
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1)

    def check_battle_end(self):
        for player in [self.player, self.bot]:
            if all(c.hp <= 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                return True
                
            if player.active_creature.hp <= 0:
                available = [c for c in player.creatures if c.hp > 0]
                if available:
                    choices = [SelectThing(c) for c in available]
                    choice = self._wait_for_choice(player, choices)
                    player.active_creature = choice.thing
                    self._show_text(player, f"{player.display_name} sent out {choice.thing.display_name}!")
        
        return False
