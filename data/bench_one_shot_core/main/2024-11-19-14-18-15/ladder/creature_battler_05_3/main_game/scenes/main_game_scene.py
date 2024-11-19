from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Reset creature HP
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

Available actions:
> Attack
{"> Swap" if self.get_available_creatures(self.player) else ""}
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
                break

    def get_available_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def get_player_action(self, player):
        while True:
            # Main menu choices
            choices = [Button("Attack")]
            available_creatures = self.get_available_creatures(player)
            if available_creatures:
                choices.append(Button("Swap"))
            
            main_choice = self._wait_for_choice(player, choices)
            
            if main_choice.display_name == "Attack":
                # Show skills with Back option
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(Button("Back"))
                
                choice = self._wait_for_choice(player, skill_choices)
                if isinstance(choice, Button):
                    continue
                return choice
            else:
                # Show creatures with Back option
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choices.append(Button("Back"))
                
                choice = self._wait_for_choice(player, creature_choices)
                if isinstance(choice, Button):
                    continue
                return choice

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
            self._show_text(self.player, f"You sent out {player_action.thing.display_name}!")
            
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            self._show_text(self.player, f"Foe sent out {bot_action.thing.display_name}!")

        # Handle attacks
        actions = []
        if isinstance(player_action.thing, Skill):
            actions.append((self.player, player_action.thing))
        if isinstance(bot_action.thing, Skill):
            actions.append((self.bot, bot_action.thing))
            
        # Sort by speed with random tiebreaking
        actions.sort(key=lambda x: (x[0].active_creature.speed, random.random()), reverse=True)
        
        # Execute attacks
        for attacker, skill in actions:
            defender = self.bot if attacker == self.player else self.player
            self.execute_skill(attacker, defender, skill)
            
            # Force swap if creature fainted
            if defender.active_creature.hp <= 0:
                available_creatures = self.get_available_creatures(defender)
                if available_creatures:
                    creature_choices = [SelectThing(creature) for creature in available_creatures]
                    new_creature = self._wait_for_choice(defender, creature_choices).thing
                    defender.active_creature = new_creature
                    self._show_text(self.player, f"{'Foe' if defender == self.bot else 'You'} sent out {new_creature.display_name}!")

    def execute_skill(self, attacker, defender, skill):
        # Calculate raw damage
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
        effectiveness = "super effective" if multiplier > 1 else "not very effective" if multiplier < 1 else "effective"
        attacker_name = "Your" if attacker == self.player else "Foe's"
        message = f"{attacker_name} {attacker.active_creature.display_name} used {skill.display_name}! "
        message += f"It's {effectiveness}! Dealt {final_damage} damage!"
        self._show_text(self.player, message)

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
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
