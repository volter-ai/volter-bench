from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creatures by setting hp to max_hp
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Initialize active creatures    
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

        # Turn state
        self.player_action = None
        self.bot_action = None

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

Your Team:
{self._format_team(self.player)}

Foe's Team:
{self._format_team(self.bot)}
"""

    def _format_team(self, player):
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" for c in player.creatures])

    def run(self):
        while True:
            # Player turn
            self._show_text(self.player, f"Your {self.player.active_creature.display_name}'s turn!")
            self.player_action = self._handle_turn(self.player)
            
            # Bot turn
            self._show_text(self.player, f"Foe's {self.bot.active_creature.display_name}'s turn!")
            self.bot_action = self._handle_turn(self.bot)
            
            # Resolve actions
            self._resolve_actions()
            
            # Check for battle end
            if self._check_battle_end():
                # Reset creatures before transitioning
                for creature in self.player.creatures:
                    creature.hp = creature.max_hp
                for creature in self.bot.creatures:
                    creature.hp = creature.max_hp
                self.player.active_creature = None
                self.bot.active_creature = None
                break

            # Force swaps for fainted creatures
            self._handle_forced_swaps()

    def _handle_turn(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self._handle_attack_choice(player)
        else:
            return self._handle_swap_choice(player)

    def _handle_attack_choice(self, player):
        back_button = Button("Back")
        choices = [SelectThing(skill) for skill in player.active_creature.skills] + [back_button]
        
        while True:
            choice = self._wait_for_choice(player, choices)
            if choice == back_button:
                return self._handle_turn(player)
            return ("attack", choice.thing)

    def _handle_swap_choice(self, player):
        back_button = Button("Back")
        valid_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in valid_creatures] + [back_button]
        
        while True:
            choice = self._wait_for_choice(player, choices)
            if choice == back_button:
                return self._handle_turn(player)
            return ("swap", choice.thing)

    def _resolve_actions(self):
        # Handle swaps first
        if self.player_action[0] == "swap":
            self.player.active_creature = self.player_action[1]
        if self.bot_action[0] == "swap":
            self.bot.active_creature = self.bot_action[1]

        # Then handle attacks
        first_player, first_action = self._determine_order()
        second_player = self.bot if first_player == self.player else self.player
        second_action = self.bot_action if first_player == self.player else self.player_action

        # Execute first action
        self._execute_action(first_player, first_action)

        # Only execute second action if the second player's creature is still alive
        if second_player.active_creature.hp > 0:
            self._execute_action(second_player, second_action)

    def _determine_order(self):
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return (self.player, self.player_action)
        elif self.bot.active_creature.speed > self.player.active_creature.speed:
            return (self.bot, self.bot_action)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_action)
            return (self.bot, self.bot_action)

    def _execute_action(self, attacker, action):
        if action[0] != "attack":
            return
            
        skill = action[1]
        defender = self.bot if attacker == self.player else self.player
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        factor = self._get_type_factor(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * factor)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}!")

    def _get_type_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _handle_forced_swaps(self):
        for player in [self.player, self.bot]:
            if player.active_creature.hp <= 0:
                valid_creatures = [c for c in player.creatures if c.hp > 0]
                if valid_creatures:
                    choices = [SelectThing(c) for c in valid_creatures]
                    choice = self._wait_for_choice(player, choices)
                    player.active_creature = choice.thing

    def _check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
