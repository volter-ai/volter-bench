from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
            attack = Button("Attack")
            swap = Button("Swap")
            choices = [attack, swap]
            
            choice = self._wait_for_choice(player, choices)
            
            if choice == attack:
                skill_choices = [Button(s.display_name) for s in player.active_creature.skills]
                skill_choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skill_choices)
                
                if skill_choice.display_name == "Back":
                    continue
                    
                return ("attack", next(s for s in player.active_creature.skills 
                                    if s.display_name == skill_choice.display_name))
                
            elif choice == swap:
                available_creatures = [c for c in player.creatures 
                                    if c != player.active_creature and c.hp > 0]
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                swap_choices = [SelectThing(c) for c in available_creatures]
                swap_choices.append(Button("Back"))
                swap_choice = self._wait_for_choice(player, swap_choices)
                
                if isinstance(swap_choice, Button):
                    continue
                    
                return ("swap", swap_choice.thing)

    def _resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            
        # Then handle attacks
        actions = []
        if player_action[0] == "attack":
            actions.append((self.player, self.bot, player_action[1]))
        if bot_action[0] == "attack":
            actions.append((self.bot, self.player, bot_action[1]))
            
        # Sort by speed
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        # Execute attacks
        for attacker, defender, skill in actions:
            damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            
            self._show_text(self.player, 
                f"{attacker.active_creature.display_name} used {skill.display_name}! "
                f"Dealt {damage} damage to {defender.active_creature.display_name}!")
            
            if defender.active_creature.hp == 0:
                self._handle_knockout(defender)

    def _calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Calculate type multiplier
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def _get_type_multiplier(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def _handle_knockout(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if not available_creatures:
            winner = self.player if player == self.bot else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            return
            
        self._show_text(self.player, 
            f"{player.active_creature.display_name} was knocked out! Choose next creature:")
        
        swap_choices = [SelectThing(c) for c in available_creatures]
        choice = self._wait_for_choice(player, swap_choices)
        player.active_creature = choice.thing

    def _check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
