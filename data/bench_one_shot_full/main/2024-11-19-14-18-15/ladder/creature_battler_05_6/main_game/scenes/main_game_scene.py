from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
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
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

Your other creatures: {[c.display_name for c in self.player.creatures if c != player_creature]}
Foe's other creatures: {[c.display_name for c in self.bot.creatures if c != bot_creature]}
"""

    def run(self):
        while True:
            # Check if either player has no valid moves
            if not self.has_valid_moves(self.player) or not self.has_valid_moves(self.bot):
                self.handle_battle_end()
                return

            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self.handle_battle_end()
                return

    def has_valid_moves(self, player):
        # Check if current creature can attack
        if player.active_creature.hp > 0:
            return True
            
        # Check if there are any creatures to swap to
        return any(c.hp > 0 for c in player.creatures if c != player.active_creature)

    def get_player_action(self, player):
        choices = []
        
        # Only show Attack if current creature isn't knocked out
        if player.active_creature.hp > 0:
            choices.append(Button("Attack"))
            
        # Only show Swap if there are creatures to swap to
        available_creatures = [c for c in player.creatures 
                             if c != player.active_creature and c.hp > 0]
        if available_creatures:
            choices.append(Button("Swap"))
            
        # If no choices, battle should have ended
        if not choices:
            return None
            
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
        if not player_action or not bot_action:
            return
            
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            
        # Then handle attacks
        first, second = self.determine_order(player_action, bot_action)
        self.execute_action(first)
        self.execute_action(second)

    def determine_order(self, player_action, bot_action):
        if isinstance(player_action.thing, Creature) or isinstance(bot_action.thing, Creature):
            return (player_action, bot_action) if isinstance(player_action.thing, Creature) else (bot_action, player_action)
            
        player_speed = self.player.active_creature.speed
        bot_speed = self.bot.active_creature.speed
        
        if player_speed > bot_speed:
            return (player_action, bot_action)
        elif bot_speed > player_speed:
            return (bot_action, player_action)
        else:
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def execute_action(self, action):
        if not action or isinstance(action.thing, Creature):
            return
            
        attacker = self.player if action.thing in self.player.active_creature.skills else self.bot
        defender = self.bot if attacker == self.player else self.player
        
        skill = action.thing
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"Dealt {damage} damage!")
        
        if defender.active_creature.hp == 0:
            self.handle_knockout(defender)

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, player):
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if available_creatures:
            swap_choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, swap_choices)
            player.active_creature = choice.thing
        
    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        return not player_has_creatures or not bot_has_creatures

    def handle_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        if player_has_creatures:
            self._show_text(self.player, "You won the battle!")
        else:
            self._show_text(self.player, "You lost the battle!")
            
        # Reset creature HP before quitting
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
            
        self._quit_whole_game()
