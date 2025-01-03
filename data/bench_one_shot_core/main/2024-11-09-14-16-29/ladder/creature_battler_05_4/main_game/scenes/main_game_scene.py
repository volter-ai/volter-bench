from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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

> Attack
> Swap (if available)
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # After showing the battle result, return to main menu
                self._transition_to_scene("MainMenuScene")
                return

    def get_valid_swap_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def get_player_action(self, player):
        while True:
            # Main choice menu
            choices = [Button("Attack")]
            valid_swap_creatures = self.get_valid_swap_creatures(player)
            if valid_swap_creatures:
                choices.append(Button("Swap"))
            
            main_choice = self._wait_for_choice(player, choices)
            
            if main_choice.display_name == "Attack":
                # Attack submenu
                choices = [SelectThing(skill) for skill in player.active_creature.skills]
                choices.append(Button("Back"))
                
                sub_choice = self._wait_for_choice(player, choices)
                
                if sub_choice.display_name == "Back":
                    continue  # Return to main menu
                else:
                    return ("attack", sub_choice.thing)
                    
            else:  # Swap
                # Swap submenu
                choices = [SelectThing(creature) for creature in valid_swap_creatures]
                choices.append(Button("Back"))
                
                sub_choice = self._wait_for_choice(player, choices)
                
                if sub_choice.display_name == "Back":
                    continue  # Return to main menu
                else:
                    return ("swap", sub_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Resolve swaps first
        for player, (action_type, target) in actions:
            if action_type == "swap":
                player.active_creature = target
                self._show_text(player, f"{player.display_name} swapped to {target.display_name}!")
        
        # Then resolve attacks
        for player, (action_type, target) in sorted(
            actions,
            key=lambda x: x[0].active_creature.speed,
            reverse=True
        ):
            if action_type == "attack":
                self.resolve_attack(player, target)
                
            # Force swap if creature fainted
            self.check_force_swap(player)

    def resolve_attack(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {final_damage} damage!")

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def check_force_swap(self, player):
        if player.active_creature.hp <= 0:
            valid_creatures = [c for c in player.creatures if c.hp > 0]
            if valid_creatures:
                choices = [SelectThing(creature) for creature in valid_creatures]
                new_creature = self._wait_for_choice(player, choices).thing
                player.active_creature = new_creature
                self._show_text(player, f"{player.display_name} sent out {new_creature.display_name}!")

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
