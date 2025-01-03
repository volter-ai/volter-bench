from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
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
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # After battle ends, return to main menu
                self._transition_to_scene("MainMenuScene")
                return

    def get_player_action(self, player):
        choices = []
        
        # Only add Attack if creature has skills
        if player.active_creature.skills:
            choices.append(Button("Attack"))
            
        # Only add Swap if there are creatures available to swap to
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if available_creatures:
            choices.append(Button("Swap"))
            
        # If somehow we have no valid actions, force an Attack if possible
        if not choices and player.active_creature.skills:
            choices.append(Button("Attack"))
            
        # Get the action type choice
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            return self._wait_for_choice(player, skill_choices)
        else:
            # Show available creatures
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            return self._wait_for_choice(player, creature_choices)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            
        # Then handle attacks
        first_player, first_action, second_player, second_action = self.determine_turn_order(
            self.player, player_action, self.bot, bot_action)
            
        self.execute_action(first_player, first_action, second_player)
        if second_player.active_creature.hp > 0:
            self.execute_action(second_player, second_action, first_player)

    def determine_turn_order(self, p1, a1, p2, a2):
        if p1.active_creature.speed > p2.active_creature.speed:
            return p1, a1, p2, a2
        elif p2.active_creature.speed > p1.active_creature.speed:
            return p2, a2, p1, a1
        else:
            if random.random() < 0.5:
                return p1, a1, p2, a2
            return p2, a2, p1, a1

    def execute_action(self, attacker, action, defender):
        if isinstance(action.thing, Skill):
            skill = action.thing
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
            
            if defender.active_creature.hp == 0:
                self.handle_fainted_creature(defender)

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def handle_fainted_creature(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, creature_choices)
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
