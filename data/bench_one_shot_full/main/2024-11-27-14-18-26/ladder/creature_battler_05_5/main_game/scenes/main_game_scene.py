from typing import List, Dict, Tuple, Optional
import random
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, create_from_game_database
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        
        # Initialize active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle Scene ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

Your Actions:
> Attack
> Swap
"""

    def _reset_creatures(self):
        """Reset all creatures to their initial state"""
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
        self.player.active_creature = None
        self.bot.active_creature = None

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Calculate type multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": multiplier = 2.0
            elif defender.creature_type == "water": multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": multiplier = 2.0
            elif defender.creature_type == "leaf": multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": multiplier = 2.0
            elif defender.creature_type == "fire": multiplier = 0.5
            
        return int(raw_damage * multiplier)

    def _get_available_creatures(self, player: Player) -> List[Creature]:
        return [c for c in player.creatures if c != player.active_creature and c.hp > 0]

    def _handle_fainted_creature(self, player: Player) -> bool:
        """Returns True if player can continue, False if they lost"""
        available = self._get_available_creatures(player)
        if not available:
            return False
            
        self._show_text(player, f"{player.active_creature.display_name} fainted! Choose a new creature!")
        choices = [SelectThing(c) for c in available]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return True

    def _execute_turn(self, first: Tuple[Optional[Player], Optional[Skill]], second: Tuple[Optional[Player], Optional[Skill]]):
        for attacker, skill in [first, second]:
            if attacker is None or skill is None:
                continue
                
            if attacker.active_creature.hp <= 0:
                continue
                
            defender = self.bot if attacker == self.player else self.player
            damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            
            self._show_text(self.player, 
                f"{attacker.active_creature.display_name} used {skill.display_name}! "
                f"Dealt {damage} damage to {defender.active_creature.display_name}!")
                
            if defender.active_creature.hp <= 0:
                if not self._handle_fainted_creature(defender):
                    self._show_text(self.player, 
                        f"{attacker.display_name} wins! {defender.display_name} has no creatures left!")
                    self._reset_creatures()  # Reset before leaving
                    self._transition_to_scene("MainMenuScene")
                    return

    def _handle_player_choice(self) -> Optional[Skill]:
        while True:
            # Main choice
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(self.player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Attack submenu
                skill_choices = [SelectThing(s) for s in self.player.active_creature.skills]
                back_button = Button("Back")
                choices = skill_choices + [back_button]
                choice = self._wait_for_choice(self.player, choices)
                
                if choice == back_button:
                    continue
                return choice.thing
            else:
                # Swap submenu
                available = self._get_available_creatures(self.player)
                if available:
                    creature_choices = [SelectThing(c) for c in available]
                    back_button = Button("Back")
                    choices = creature_choices + [back_button]
                    choice = self._wait_for_choice(self.player, choices)
                    
                    if choice == back_button:
                        continue
                        
                    self.player.active_creature = choice.thing
                    self._show_text(self.player, f"Go, {self.player.active_creature.display_name}!")
                    return None

    def run(self):
        while True:
            # Player turn
            player_action = self._handle_player_choice()
            
            # Bot turn
            bot_action = self.bot.active_creature.skills[0]  # Simple AI - always uses first skill
            
            # Determine order and execute
            if player_action:  # If player attacked
                if self.player.active_creature.speed > self.bot.active_creature.speed:
                    self._execute_turn((self.player, player_action), (self.bot, bot_action))
                elif self.player.active_creature.speed < self.bot.active_creature.speed:
                    self._execute_turn((self.bot, bot_action), (self.player, player_action))
                else:  # Speed tie - random order
                    if random.choice([True, False]):
                        self._execute_turn((self.player, player_action), (self.bot, bot_action))
                    else:
                        self._execute_turn((self.bot, bot_action), (self.player, player_action))
            else:  # If player swapped
                self._execute_turn((self.bot, bot_action), (None, None))
