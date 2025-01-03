from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
import random
from typing import Optional, Dict

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Reset all creature HP
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

Your other creatures:
{self._format_bench_creatures(self.player)}

Foe's other creatures:
{self._format_bench_creatures(self.bot)}
"""

    def _format_bench_creatures(self, player):
        return "\n".join([f"- {c.display_name}: HP {c.hp}/{c.max_hp}" 
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
            first_action, second_action, first_actor, second_actor = self._determine_action_order(
                self.player, player_action, 
                self.bot, bot_action
            )
            
            self._resolve_actions(
                first_action, first_actor,
                second_action, second_actor
            )
            
            # Check for battle end
            if self._check_battle_end():
                return

    def _handle_turn(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                skills = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skills + [back_button])
                
                if skill_choice == back_button:
                    continue
                    
                return {"type": "attack", "skill": skill_choice.thing}
                
            elif choice == swap_button:
                available_creatures = [
                    SelectThing(creature) 
                    for creature in player.creatures 
                    if creature != player.active_creature and creature.hp > 0
                ]
                
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, available_creatures + [back_button])
                
                if creature_choice == back_button:
                    continue
                    
                return {"type": "swap", "creature": creature_choice.thing}

    def _resolve_actions(self, first_action, first_actor, second_action, second_actor):
        # Handle swaps first
        if first_action["type"] == "swap":
            first_actor.active_creature = first_action["creature"]
            self._show_text(self.player, 
                f"{'You' if first_actor == self.player else 'Foe'} switched to {first_action['creature'].display_name}!")
            
        if second_action["type"] == "swap":
            second_actor.active_creature = second_action["creature"]
            self._show_text(self.player,
                f"{'You' if second_actor == self.player else 'Foe'} switched to {second_action['creature'].display_name}!")

        # Then handle attacks
        if first_action["type"] == "attack":
            self._execute_action(first_action, first_actor)
        if second_action["type"] == "attack":
            self._execute_action(second_action, second_actor)

    def _determine_action_order(self, player, player_action, bot, bot_action):
        if player_action["type"] == "swap" or bot_action["type"] == "swap":
            return player_action, bot_action, player, bot
            
        player_speed = player.active_creature.speed
        bot_speed = bot.active_creature.speed
        
        if player_speed > bot_speed:
            return player_action, bot_action, player, bot
        elif bot_speed > player_speed:
            return bot_action, player_action, bot, player
        else:
            if random.random() < 0.5:
                return player_action, bot_action, player, bot
            return bot_action, player_action, bot, player

    def _execute_action(self, action, attacker):
        if action["type"] != "attack":
            return
            
        defender = self.bot if attacker == self.player else self.player
        
        skill = action["skill"]
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
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

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
        self._show_text(self.player, f"{player.active_creature.display_name} was knocked out!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if not available_creatures:
            return
            
        choices = [SelectThing(c) for c in available_creatures]
        choice = self._wait_for_choice(player, choices)
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
