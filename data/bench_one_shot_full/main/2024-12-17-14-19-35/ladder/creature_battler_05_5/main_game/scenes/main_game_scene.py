from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
from typing import Tuple, Optional

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures directly
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

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                if not any(c.hp > 0 for c in self.player.creatures):
                    self._show_text(self.player, "You lost the battle!")
                else:
                    self._show_text(self.player, "You won the battle!")
                self._quit_whole_game()
                return
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                self._show_text(self.player, "You won the battle!")
                self._quit_whole_game()
                return
                
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()
                return

    def get_player_action(self, player) -> Optional[Tuple[str, any]]:
        if player.active_creature.hp <= 0:
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            if not available_creatures:
                return None
            
            choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            return ("swap", choice.thing)
            
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")
        
        while True:
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                skill_choices = [SelectThing(s) for s in player.active_creature.skills]
                skill_choices.append(back_button)
                skill_choice = self._wait_for_choice(player, skill_choices)
                if skill_choice != back_button:
                    return ("attack", skill_choice.thing)
                    
            elif choice == swap_button:
                available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                if available_creatures:
                    creature_choices = [SelectThing(c) for c in available_creatures]
                    creature_choices.append(back_button)
                    creature_choice = self._wait_for_choice(player, creature_choices)
                    if creature_choice != back_button:
                        player.active_creature = creature_choice.thing
                        return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action: Tuple[str, any], bot_action: Tuple[str, any]):
        # Handle swaps first
        if player_action[0] == "swap":
            self._show_text(self.player, f"You switched to {player_action[1].display_name}!")
        if bot_action[0] == "swap":
            self._show_text(self.player, f"Foe switched to {bot_action[1].display_name}!")
            
        # Then handle attacks
        actions = []
        if player_action[0] == "attack":
            actions.append((self.player, player_action[1], self.bot))
        if bot_action[0] == "attack":
            actions.append((self.bot, bot_action[1], self.player))
            
        # Sort by speed
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        # Execute attacks
        for attacker, skill, defender in actions:
            damage = self.calculate_damage(attacker.active_creature, skill, defender.active_creature)
            defender.active_creature.hp -= damage
            self._show_text(self.player, 
                f"{attacker.active_creature.display_name} used {skill.display_name}! "
                f"Dealt {damage} damage to {defender.active_creature.display_name}!")

    def calculate_damage(self, attacker, skill, defender) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Calculate type multiplier
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
