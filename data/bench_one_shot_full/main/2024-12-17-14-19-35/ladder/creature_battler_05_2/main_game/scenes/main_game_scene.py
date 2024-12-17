from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
from typing import Tuple, Optional

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creatures by setting hp to max_hp
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

Your Team:
{self._format_team(self.player)}

Foe's Team:
{self._format_team(self.bot)}
"""

    def _format_team(self, player):
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" for c in player.creatures])

    def run(self):
        while True:
            # Player and bot make choices
            player_action = self._get_player_action(self.player)
            bot_action = self._get_player_action(self.bot)
            
            # Resolve actions
            self._resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                # Reset creatures before leaving scene
                for creature in self.player.creatures:
                    creature.hp = creature.max_hp
                for creature in self.bot.creatures:
                    creature.hp = creature.max_hp
                self.player.active_creature = None
                self.bot.active_creature = None
                
                # Return to main menu
                self._transition_to_scene("MainMenuScene")
                return

    def _get_player_action(self, player):
        if player.active_creature.hp <= 0:
            return self._force_swap(player)
            
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self._choose_attack(player)
        else:
            return self._choose_swap(player)

    def _choose_attack(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button):
            return self._get_player_action(player)
        return ("attack", choice.thing)

    def _choose_swap(self, player):
        valid_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        if not valid_creatures:
            return self._get_player_action(player)
            
        choices = [SelectThing(creature) for creature in valid_creatures]
        choices.append(Button("Back"))
        
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button):
            return self._get_player_action(player)
        return ("swap", choice.thing)

    def _force_swap(self, player):
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        if not valid_creatures:
            return None
            
        choices = [SelectThing(creature) for creature in valid_creatures]
        choice = self._wait_for_choice(player, choices)
        return ("swap", choice.thing)

    def _resolve_turn(self, player_action, bot_action):
        if not player_action or not bot_action:
            return
            
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"You sent out {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Foe sent out {bot_action[1].display_name}!")

        # Then handle attacks
        if player_action[0] == "attack" and bot_action[0] == "attack":
            # Determine order based on speed
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                first = (self.player, player_action[1])
                second = (self.bot, bot_action[1])
            elif self.bot.active_creature.speed > self.player.active_creature.speed:
                first = (self.bot, bot_action[1])
                second = (self.player, player_action[1])
            else:
                # Random if speeds are equal
                if random.random() < 0.5:
                    first = (self.player, player_action[1])
                    second = (self.bot, bot_action[1])
                else:
                    first = (self.bot, bot_action[1])
                    second = (self.player, player_action[1])

            # Execute first attack
            self._execute_attack(*first)
            
            # Get defender from first attack
            defender = self.bot if first[0] == self.player else self.player
            
            # Only do second attack if defender's creature is still alive
            if defender.active_creature.hp > 0:
                self._execute_attack(*second)

    def _execute_attack(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show message
        effectiveness = "It's super effective!" if multiplier > 1 else "It's not very effective..." if multiplier < 1 else ""
        self._show_text(self.player, 
            f"{'You' if attacker == self.player else 'Foe'} used {skill.display_name}! {effectiveness}")

    def _get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
