from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Creature, Player
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Reset creature HP
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = None
            while player_action is None:  # Keep asking until valid action
                player_action = self.get_player_action(self.player)
                
            # Bot turn - bots don't get "Back" option
            bot_action = self.get_bot_action()
            
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Properly end the game using engine method
                self._quit_whole_game()

    def get_player_action(self, player: Player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            skill_choices.append(back_button)
            choice = self._wait_for_choice(player, skill_choices)
            if choice == back_button:
                return None
            return ("attack", choice.thing)
            
        elif choice == swap_button:
            # Show available creatures
            available_creatures = [c for c in player.creatures 
                                if c != player.active_creature and c.hp > 0]
            if not available_creatures:
                self._show_text(player, "No creatures available to swap!")
                return None
                
            creature_choices = [SelectThing(c) for c in available_creatures]
            creature_choices.append(back_button)
            choice = self._wait_for_choice(player, creature_choices)
            if choice == back_button:
                return None
            return ("swap", choice.thing)

    def get_bot_action(self):
        """Simplified bot AI that doesn't use "Back" option"""
        # If current creature has low HP, try to swap
        if self.bot.active_creature.hp < self.bot.active_creature.max_hp * 0.3:
            available_creatures = [c for c in self.bot.creatures 
                                if c != self.bot.active_creature and c.hp > 0]
            if available_creatures:
                return ("swap", random.choice(available_creatures))
        
        # Otherwise attack with random skill
        return ("attack", random.choice(self.bot.active_creature.skills))

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.execute_swap(self.player, player_action[1])
        if bot_action[0] == "swap":
            self.execute_swap(self.bot, bot_action[1])
                
        # Then handle attacks
        if player_action[0] == "attack" and bot_action[0] == "attack":
            if self.player.active_creature.speed >= self.bot.active_creature.speed:
                self.execute_attack(self.player, self.bot, player_action[1])
                if self.bot.active_creature.hp > 0:
                    self.execute_attack(self.bot, self.player, bot_action[1])
            else:
                self.execute_attack(self.bot, self.player, bot_action[1])
                if self.player.active_creature.hp > 0:
                    self.execute_attack(self.player, self.bot, player_action[1])

    def execute_attack(self, attacker: Player, defender: Player, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {final_damage} damage!")
        
        if defender.active_creature.hp == 0:
            self.handle_fainted_creature(defender)

    def execute_swap(self, player: Player, new_creature: Creature):
        player.active_creature = new_creature
        self._show_text(player, f"Swapped to {new_creature.display_name}!")

    def get_type_effectiveness(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)

    def handle_fainted_creature(self, player: Player):
        self._show_text(player, f"{player.active_creature.display_name} fainted!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        creature_choices = [SelectThing(c) for c in available_creatures]
        choice = self._wait_for_choice(player, creature_choices)
        self.execute_swap(player, choice.thing)

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
