from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        for p in [self.player, self.bot]:
            p.active_creature = p.creatures[0]
            for c in p.creatures:
                c.hp = c.max_hp

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle Scene ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

Your other creatures:
{self._format_bench(self.player)}

Foe's other creatures:
{self._format_bench(self.bot)}
"""

    def _format_bench(self, player):
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" 
                         for c in player.creatures if c != player.active_creature])

    def run(self):
        while True:
            # Player turn
            player_action = self._handle_turn_choice(self.player)
            if not player_action:
                return
                
            # Bot turn
            bot_action = self._handle_turn_choice(self.bot)
            if not bot_action:
                return
                
            # Resolve actions
            self._resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                return

    def _handle_turn_choice(self, player):
        if not self._has_valid_creatures(player):
            return None
            
        attack = Button("Attack")
        swap = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack, swap])
        
        if choice == attack:
            return self._handle_attack_choice(player)
        else:
            return self._handle_swap_choice(player)

    def _handle_attack_choice(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button):
            return self._handle_turn_choice(player)
            
        return ("attack", choice.thing)

    def _handle_swap_choice(self, player):
        valid_creatures = [c for c in player.creatures 
                         if c != player.active_creature and c.hp > 0]
        
        if not valid_creatures:
            self._show_text(player, "No valid creatures to swap to!")
            return self._handle_turn_choice(player)
            
        choices = [SelectThing(c) for c in valid_creatures]
        choices.append(Button("Back"))
        
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button):
            return self._handle_turn_choice(player)
            
        return ("swap", choice.thing)

    def _resolve_actions(self, p_action, b_action):
        # Handle swaps first
        if p_action[0] == "swap":
            self.player.active_creature = p_action[1]
        if b_action[0] == "swap":
            self.bot.active_creature = b_action[1]
            
        # Then handle attacks
        actions = [(self.player, p_action), (self.bot, b_action)]
        
        # Sort by speed for attack order
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        if actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
            random.shuffle(actions)
            
        for attacker, action in actions:
            if action[0] == "attack":
                defender = self.bot if attacker == self.player else self.player
                self._execute_attack(attacker, defender, action[1])

    def _execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         defender.active_creature.defense)
        else:
            raw_damage = (skill.base_damage * 
                         attacker.active_creature.sp_attack / 
                         defender.active_creature.sp_defense)
            
        # Apply type effectiveness
        factor = self._get_type_factor(skill.skill_type, 
                                     defender.active_creature.creature_type)
        
        final_damage = int(raw_damage * factor)
        defender.active_creature.hp -= max(1, final_damage)
        
        self._show_text(attacker, 
            f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender,
            f"{defender.active_creature.display_name} took {final_damage} damage!")

    def _get_type_factor(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def _has_valid_creatures(self, player):
        if player.active_creature.hp <= 0:
            valid_creatures = [c for c in player.creatures if c.hp > 0]
            if not valid_creatures:
                return False
                
            choices = [SelectThing(c) for c in valid_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            
        return True

    def _check_battle_end(self):
        p_valid = any(c.hp > 0 for c in self.player.creatures)
        b_valid = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_valid or not b_valid:
            winner = self.player if p_valid else self.bot
            self._show_text(self.player, 
                "You win!" if winner == self.player else "You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
