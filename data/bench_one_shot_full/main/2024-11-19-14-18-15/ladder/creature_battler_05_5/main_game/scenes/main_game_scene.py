from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Creature, Player
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
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player):
        # Get available creatures for swapping
        available_creatures = [
            creature 
            for creature in player.creatures 
            if creature != player.active_creature and creature.hp > 0
        ]
        
        # Build choice list based on available options
        choices = [Button("Attack")]
        if available_creatures:
            choices.append(Button("Swap"))
        
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            # Show skills with Back option
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            back_button = Button("Back")
            skill_choices.append(back_button)
            
            skill_choice = self._wait_for_choice(player, skill_choices)
            
            # If Back was chosen, recurse to main menu
            if skill_choice == back_button:
                return self.get_player_action(player)
            return skill_choice
            
        else:  # Swap was chosen
            # Show available creatures with Back option
            swap_choices = [SelectThing(creature) for creature in available_creatures]
            back_button = Button("Back")
            swap_choices.append(back_button)
            
            swap_choice = self._wait_for_choice(player, swap_choices)
            
            # If Back was chosen, recurse to main menu
            if swap_choice == back_button:
                return self.get_player_action(player)
            return swap_choice

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            
        # Determine order for attacks
        first = self.player
        second = self.bot
        if self.bot.active_creature.speed > self.player.active_creature.speed:
            first, second = second, first
        elif self.bot.active_creature.speed == self.player.active_creature.speed:
            if random.random() < 0.5:
                first, second = second, first
                
        # Execute attacks
        for attacker, action in [(first, player_action if first == self.player else bot_action),
                               (second, bot_action if second == self.bot else player_action)]:
            if isinstance(action.thing, Creature):
                continue
                
            skill = action.thing
            target = self.bot.active_creature if attacker == self.player else self.player.active_creature
            
            damage = self.calculate_damage(skill, attacker.active_creature, target)
            target.hp = max(0, target.hp - damage)
            
            self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
            self._show_text(attacker, f"Dealt {damage} damage!")
            
            if target.hp == 0:
                self.handle_knockout(self.bot if attacker == self.player else self.player)

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

    def handle_knockout(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        
        if not available_creatures:
            return
            
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        swap_choices = [SelectThing(c) for c in available_creatures]
        choice = self._wait_for_choice(player, swap_choices)
        player.active_creature = choice.thing

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            winner = self.player if player_alive else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
