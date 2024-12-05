from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
from typing import List, Tuple
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
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
                # Instead of just returning, properly end the game
                self._quit_whole_game()

    def get_player_action(self, player: Player) -> Tuple[str, Skill | Creature]:
        # Get available creatures for swapping
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        
        # Build choice list
        choices = [Button("Attack")]
        if available_creatures:  # Only show swap if there are creatures to swap to
            choices.append(Button("Swap"))
        
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            skill_choice = self._wait_for_choice(player, skill_choices)
            return ("attack", skill_choice.thing)
        else:
            # Show available creatures
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            creature_choice = self._wait_for_choice(player, creature_choices)
            return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action: Tuple[str, Skill | Creature], bot_action: Tuple[str, Skill | Creature]):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]

        # Then handle attacks
        first_player, first_action, second_player, second_action = self.determine_turn_order(
            self.player, player_action, self.bot, bot_action)
        
        if first_action[0] == "attack":
            self.execute_attack(first_player, second_player, first_action[1])
        if second_action[0] == "attack" and second_player.active_creature.hp > 0:
            self.execute_attack(second_player, first_player, second_action[1])

    def determine_turn_order(self, p1: Player, a1: Tuple, p2: Player, a2: Tuple):
        if a1[0] == "swap" or a2[0] == "swap":
            return (p1, a1, p2, a2)
        
        if p1.active_creature.speed > p2.active_creature.speed:
            return (p1, a1, p2, a2)
        elif p2.active_creature.speed > p1.active_creature.speed:
            return (p2, a2, p1, a1)
        else:
            if random.random() < 0.5:
                return (p1, a1, p2, a2)
            return (p2, a2, p1, a1)

    def execute_attack(self, attacker: Player, defender: Player, skill: Skill):
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
        
        # Show result
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"It dealt {final_damage} damage!")
        
        # Handle fainted creature
        if defender.active_creature.hp == 0:
            self.handle_fainted_creature(defender)

    def get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def handle_fainted_creature(self, player: Player):
        self._show_text(player, f"{player.active_creature.display_name} fainted!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing
            self._show_text(player, f"Go, {player.active_creature.display_name}!")

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
