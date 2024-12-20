from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
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

Available actions:
> Attack (if creature has skills)
> Swap (if you have other creatures with HP)"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            self.check_battle_end()

    def get_available_actions(self, player):
        actions = []
        
        # Only show Attack if creature has skills
        if player.active_creature.skills:
            actions.append(Button("Attack"))
            
        # Only show Swap if there are valid creatures to swap to
        valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if valid_creatures:
            actions.append(Button("Swap"))
            
        # If somehow no actions are available (shouldn't happen with current data),
        # give attack option which will then show skills
        if not actions:
            actions.append(Button("Attack"))
            
        return actions

    def get_player_action(self, player):
        # Get available actions
        actions = self.get_available_actions(player)
        choice = self._wait_for_choice(player, actions)
        
        if choice.display_name == "Attack":
            # Ensure creature has skills before offering choices
            if not player.active_creature.skills:
                self._show_text(player, f"{player.active_creature.display_name} has no skills!")
                return self.get_player_action(player)
                
            choices = [SelectThing(skill) for skill in player.active_creature.skills]
            return self._wait_for_choice(player, choices)
        else:  # Swap
            valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            choices = [SelectThing(creature) for creature in valid_creatures]
            return self._wait_for_choice(player, choices)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            
        # Then handle attacks
        first, second = self.get_action_order(player_action, bot_action)
        self.execute_action(first)
        self.execute_action(second)

    def get_action_order(self, player_action, bot_action):
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_action, bot_action
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return bot_action, player_action
        else:
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def execute_action(self, action):
        if isinstance(action.thing, Creature):
            return
            
        skill = action.thing
        attacker = self.player if action.thing in self.player.active_creature.skills else self.bot
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
        
        # Force swap if creature fainted
        if defender.active_creature.hp == 0:
            valid_creatures = [c for c in defender.creatures if c.hp > 0]
            if valid_creatures:
                choices = [SelectThing(creature) for creature in valid_creatures]
                new_creature = self._wait_for_choice(defender, choices).thing
                defender.active_creature = new_creature

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
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost!")
            self._transition_to_scene("MainMenuScene")
        elif not bot_has_creatures:
            self._show_text(self.player, "You won!")
            self._transition_to_scene("MainMenuScene")
