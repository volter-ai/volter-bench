from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Creature
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
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

Your other creatures:
{self._format_bench_creatures(self.player)}

Foe's other creatures:
{self._format_bench_creatures(self.bot)}

> Attack
> Swap
"""

    def _format_bench_creatures(self, player):
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" 
                         for c in player.creatures if c != player.active_creature])

    def run(self):
        while True:
            # Player turn
            player_action = self._handle_turn(self.player)
            if not player_action:
                return
                
            # Bot turn
            bot_action = self._handle_turn(self.bot)
            if not bot_action:
                return
                
            # Resolve actions
            self._resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                return

    def _handle_turn(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(player, [attack_button, swap_button])

            if choice == attack_button:
                skills = player.active_creature.skills
                skill_choices = [SelectThing(skill) for skill in skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skill_choices + [back_button])
                
                if skill_choice == back_button:
                    continue
                    
                return ("attack", skill_choice.thing)

            elif choice == swap_button:
                available_creatures = [c for c in player.creatures 
                                    if c != player.active_creature and c.hp > 0]
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, creature_choices + [back_button])
                
                if creature_choice == back_button:
                    continue
                    
                return ("swap", creature_choice.thing)

    def _resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"You switched to {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Foe switched to {bot_action[1].display_name}!")

        # Then handle attacks
        actions = []
        if player_action[0] == "attack":
            actions.append((self.player, player_action[1]))
        if bot_action[0] == "attack":
            actions.append((self.bot, bot_action[1]))
            
        # Sort by speed
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        if len(actions) == 2 and actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
            random.shuffle(actions)
            
        # Execute attacks
        for attacker, skill in actions:
            defender = self.bot if attacker == self.player else self.player
            self._execute_attack(attacker, defender, skill)

    def _execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         defender.active_creature.defense)
        else:
            raw_damage = (attacker.active_creature.sp_attack / 
                         defender.active_creature.sp_defense * 
                         skill.base_damage)
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, 
                                             defender.active_creature.creature_type)
        
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
                       f"{attacker.active_creature.display_name} used {skill.display_name}! "
                       f"Dealt {final_damage} damage!")
        
        if defender.active_creature.hp == 0:
            self._handle_knockout(defender)

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _handle_knockout(self, player):
        self._show_text(self.player, 
                       f"{player.active_creature.display_name} was knocked out!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        
        self._show_text(self.player,
                       f"{'You' if player == self.player else 'Foe'} sent out {choice.thing.display_name}!")

    def _check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            winner = "You" if player_alive else "Foe"
            self._show_text(self.player, f"{winner} won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
