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

Your Team: {', '.join(c.display_name for c in self.player.creatures if c.hp > 0)}
Foe's Team: {', '.join(c.display_name for c in self.bot.creatures if c.hp > 0)}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_action = self.get_player_action(self.player)
            
            # Bot Choice Phase  
            bot_action = self.get_player_action(self.bot)
            
            # Resolution Phase
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Reset creatures before transitioning
                for creature in self.player.creatures + self.bot.creatures:
                    creature.hp = creature.max_hp
                self._transition_to_scene("MainMenuScene")
                return

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Show skills
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                choice = self._wait_for_choice(player, skill_choices + [back_button])
                
                if choice != back_button:
                    return ("attack", choice.thing)
                    
            else:
                # Show available creatures
                available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                back_button = Button("Back")
                choice = self._wait_for_choice(player, creature_choices + [back_button])
                
                if choice != back_button:
                    return ("swap", choice.thing)

    def resolve_actions(self, player_action, bot_action):
        # Determine order
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Swaps go first
        actions.sort(key=lambda x: 0 if x[1][0] == "swap" else 1)
        
        # For attacks, faster creature goes first
        if actions[0][1][0] == "attack" and actions[1][1][0] == "attack":
            if actions[0][0].active_creature.speed < actions[1][0].active_creature.speed:
                actions.reverse()
            elif actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
                if random.random() < 0.5:
                    actions.reverse()
        
        # Execute actions
        for player, action in actions:
            action_type, thing = action
            if action_type == "swap":
                old_creature = player.active_creature
                player.active_creature = thing
                self._show_text(player, f"{old_creature.display_name} swapped out for {thing.display_name}!")
            else:
                self.execute_skill(player, thing)
                
            # Force swap if active creature fainted
            self.check_force_swap(self.player)
            self.check_force_swap(self.bot)

    def execute_skill(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"Dealt {final_damage} damage!")

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)

    def check_force_swap(self, player):
        if player.active_creature.hp <= 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if available_creatures:
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
                choice = self._wait_for_choice(player, creature_choices)
                player.active_creature = choice.thing
                self._show_text(player, f"Sent out {choice.thing.display_name}!")

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures or not bot_has_creatures:
            if player_has_creatures:
                self._show_text(self.player, "You won!")
            else:
                self._show_text(self.player, "You lost!")
            return True
            
        return False
