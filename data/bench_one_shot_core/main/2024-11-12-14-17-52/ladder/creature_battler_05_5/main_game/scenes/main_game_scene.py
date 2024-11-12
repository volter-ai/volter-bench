from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Reset creature HP
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Check if either player has no valid moves
            if player_action is None or bot_action is None:
                if not self.check_battle_end():
                    # If battle isn't over but no valid moves, force swap
                    self.force_swaps()
                continue
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            battle_result = self.check_battle_end()
            if battle_result:
                if battle_result == "win":
                    self._show_text(self.player, "You won the battle!")
                    self._transition_to_scene("MainMenuScene")
                else:
                    self._show_text(self.player, "You lost the battle!")
                    self._quit_whole_game()
                return

    def get_player_action(self, player):
        # For bots, skip the back button logic
        if isinstance(player._listener, BotListener):
            return self._get_player_action_simple(player)
            
        while True:
            # First check if player can make any action
            can_attack = len(player.active_creature.skills) > 0
            can_swap = any(c.hp > 0 and c != player.active_creature for c in player.creatures)
            
            if not (can_attack or can_swap):
                return None
                
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choices = []
            if can_attack:
                choices.append(attack_button)
            if can_swap:
                choices.append(swap_button)
                
            main_choice = self._wait_for_choice(player, choices)
            
            if main_choice == attack_button:
                action = self.get_attack_choice(player)
                if action:  # Only return if we got an action (not backed out)
                    return action
            else:
                action = self.get_swap_choice(player)
                if action:  # Only return if we got an action (not backed out)
                    return action

    def _get_player_action_simple(self, player):
        """Simplified version without back button for bots"""
        can_attack = len(player.active_creature.skills) > 0
        can_swap = any(c.hp > 0 and c != player.active_creature for c in player.creatures)
        
        if not (can_attack or can_swap):
            return None
            
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choices = []
        if can_attack:
            choices.append(attack_button)
        if can_swap:
            choices.append(swap_button)
            
        choice = self._wait_for_choice(player, choices)
        
        if choice == attack_button:
            return self.get_attack_choice(player, include_back=False)
        else:
            return self.get_swap_choice(player, include_back=False)

    def get_attack_choice(self, player, include_back=True):
        if not player.active_creature.skills:
            return None
            
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        if include_back:
            choices.append(Button("Back"))
            
        choice = self._wait_for_choice(player, choices)
        
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return ("attack", choice.thing)

    def get_swap_choice(self, player, include_back=True):
        valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not valid_creatures:
            return None
            
        choices = [SelectThing(creature) for creature in valid_creatures]
        if include_back:
            choices.append(Button("Back"))
            
        choice = self._wait_for_choice(player, choices)
        
        if isinstance(choice, Button) and choice.display_name == "Back":
            return None
        return ("swap", choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Both actions should be valid at this point
        if player_action is None or bot_action is None:
            return
            
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
        
        for attacker, defender, skill in actions:
            self.execute_skill(attacker.active_creature, defender.active_creature, skill)
            if defender.active_creature.hp <= 0:
                self.handle_fainted_creature(defender)

    def force_swaps(self):
        """Force players to swap if they have any valid creatures to swap to"""
        for player in [self.player, self.bot]:
            if player.active_creature.hp <= 0:
                self.handle_fainted_creature(player)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        final_damage = int(raw_damage * multiplier)
        defender.hp = max(0, defender.hp - final_damage)

        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage!")

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_fainted_creature(self, player):
        self._show_text(self.player, f"{player.active_creature.display_name} fainted!")
        
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        if valid_creatures:
            choices = [SelectThing(creature) for creature in valid_creatures]
            player.active_creature = self._wait_for_choice(player, choices).thing

    def check_battle_end(self) -> str | None:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            return "lose"
        elif not bot_has_creatures:
            return "win"
            
        return None
