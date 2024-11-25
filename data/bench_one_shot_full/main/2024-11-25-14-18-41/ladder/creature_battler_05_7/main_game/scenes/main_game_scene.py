from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
Your Active: {self.player.active_creature.display_name} ({self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP)
Foe's Active: {self.bot.active_creature.display_name} ({self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP)

Your Team:
{player_creatures_status}

Foe's Team:
{bot_creatures_status}

> Attack
> Swap (if available)
> Back
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Reset creature HP before transitioning
                for creature in self.player.creatures:
                    creature.hp = creature.max_hp
                for creature in self.bot.creatures:
                    creature.hp = creature.max_hp
                    
                # Return to main menu
                self._transition_to_scene("MainMenuScene")
                return

    def get_available_creatures(self, player):
        return [
            c for c in player.creatures 
            if c != player.active_creature and c.hp > 0
        ]

    def get_player_action(self, player):
        while True:
            # Main choice
            choices = [Button("Attack")]
            available_creatures = self.get_available_creatures(player)
            if available_creatures:
                choices.append(Button("Swap"))
            
            choice = self._wait_for_choice(player, choices)
            
            if choice.display_name == "Attack":
                # Show skills with Back option
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(Button("Back"))
                
                skill_choice = self._wait_for_choice(player, skill_choices)
                if skill_choice.display_name == "Back":
                    continue  # Go back to main choices
                return skill_choice
                
            else:  # Swap
                # Show creatures with Back option
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choices.append(Button("Back"))
                
                creature_choice = self._wait_for_choice(player, creature_choices)
                if creature_choice.display_name == "Back":
                    continue  # Go back to main choices
                return creature_choice

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, type(self.player.creatures[0])):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, type(self.bot.creatures[0])):
            self.bot.active_creature = bot_action.thing

        # Then handle attacks
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Sort by speed, with random resolution for ties
        actions.sort(key=lambda x: (
            x[0].active_creature.speed, 
            random.random()  # Secondary sort key for random tie resolution
        ), reverse=True)
        
        for attacker, action in actions:
            if isinstance(action.thing, type(self.player.creatures[0].skills[0])):
                defender = self.bot if attacker == self.player else self.player
                self.execute_skill(action.thing, attacker, defender)

    def execute_skill(self, skill, attacker, defender):
        # Calculate damage
        if skill.is_physical:
            raw_damage = (
                attacker.active_creature.attack + 
                skill.base_damage - 
                defender.active_creature.defense
            )
        else:
            raw_damage = (
                skill.base_damage * 
                attacker.active_creature.sp_attack / 
                defender.active_creature.sp_defense
            )

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(
            skill.skill_type, 
            defender.active_creature.creature_type
        )
        
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)

        self._show_text(
            self.player,
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage!"
        )

        # Handle fainting
        if defender.active_creature.hp <= 0:
            self.handle_fainted_creature(defender)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_fainted_creature(self, player):
        available_creatures = self.get_available_creatures(player)
        
        if available_creatures:
            self._show_text(
                self.player,
                f"{player.active_creature.display_name} fainted!"
            )
            
            choice = self._wait_for_choice(player, [
                SelectThing(creature) for creature in available_creatures
            ])
            player.active_creature = choice.thing

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
