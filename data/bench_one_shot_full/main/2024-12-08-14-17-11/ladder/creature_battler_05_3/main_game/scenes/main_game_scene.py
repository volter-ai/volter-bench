from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP" 
            for c in self.player.creatures
        )
        bot_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP"
            for c in self.bot.creatures
        )
        
        return f"""=== Battle ===
Your Team:
{player_creatures_status}
Active: {self.player.active_creature.display_name}

Opponent's Team: 
{bot_creatures_status}
Active: {self.bot.active_creature.display_name}

> Attack
> Swap (if available)"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:  # No valid actions means no living creatures
                break
                
            bot_action = self.get_player_action(self.bot)
            if not bot_action:  # No valid actions means no living creatures
                break
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_available_creatures(self, player):
        return [c for c in player.creatures 
                if c != player.active_creature and c.hp > 0]

    def get_player_action(self, player):
        while True:
            choices = []
            
            # Always offer Attack option if creature has skills
            if player.active_creature and player.active_creature.hp > 0:
                choices.append(Button("Attack"))
                
                # Only offer Swap if there are creatures to swap to
                if self.get_available_creatures(player):
                    choices.append(Button("Swap"))
            
            # If no choices possible, player has lost
            if not choices:
                return None
                
            main_choice = self._wait_for_choice(player, choices)
            
            if main_choice.display_name == "Attack":
                # Show skills with Back option
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choices.append(back_button)
                
                choice = self._wait_for_choice(player, skill_choices)
                if choice == back_button:
                    continue
                return choice
            else:
                # Show available creatures with Back option
                available_creatures = self.get_available_creatures(player)
                creature_choices = [SelectThing(c) for c in available_creatures]
                back_button = Button("Back")
                creature_choices.append(back_button)
                
                choice = self._wait_for_choice(player, creature_choices)
                if choice == back_button:
                    continue
                return choice

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
            self._show_text(self.player, f"You swapped to {player_action.thing.display_name}!")
            
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            self._show_text(self.player, f"Opponent swapped to {bot_action.thing.display_name}!")

        # Determine turn order
        first = self.player
        second = self.bot
        first_action = player_action
        second_action = bot_action

        # If speeds are equal, randomly choose who goes first
        if self.bot.active_creature.speed == self.player.active_creature.speed:
            if random.choice([True, False]):
                first = self.bot
                second = self.player
                first_action = bot_action
                second_action = player_action
        # Otherwise faster creature goes first
        elif self.bot.active_creature.speed > self.player.active_creature.speed:
            first = self.bot
            second = self.player
            first_action = bot_action
            second_action = player_action

        self.execute_action(first, second, first_action)
        if second.active_creature.hp > 0:
            self.execute_action(second, first, second_action)

    def execute_action(self, attacker, defender, action):
        if isinstance(action.thing, Creature):
            return

        skill = action.thing
        target = defender.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - target.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / target.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, target.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        target.hp = max(0, target.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {target.display_name}!")

        if target.hp == 0:
            self._show_text(self.player, f"{target.display_name} was knocked out!")
            self.handle_knockout(defender)

    def get_type_effectiveness(self, skill_type, target_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        
        return effectiveness.get((skill_type, target_type), 1.0)

    def handle_knockout(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        creature_choices = [SelectThing(c) for c in available_creatures]
        new_creature = self._wait_for_choice(player, creature_choices).thing
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} sent out {new_creature.display_name}!")

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            winner = self.player if player_alive else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            
            # Reset creatures
            for creature in self.player.creatures:
                creature.hp = creature.max_hp
            for creature in self.bot.creatures:
                creature.hp = creature.max_hp
                
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
