from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Player
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

What will you do?
> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Return to main menu after battle ends
                self._transition_to_scene("MainMenuScene")
                return

    def get_player_action(self, player: Player):
        # Get available creatures for swap
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        
        # Build choice list based on available options
        choices = []
        if player.active_creature.skills:  # If creature has skills
            choices.append(Button("Attack"))
        if available_creatures:  # Only show swap if there are creatures to swap to
            choices.append(Button("Swap"))
            
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            return self._wait_for_choice(player, skill_choices)
        else:
            # Show available creatures
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            return self._wait_for_choice(player, creature_choices)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            
        # Determine order for attacks
        first = self.player
        second = self.bot
        if self.bot.active_creature.speed > self.player.active_creature.speed:
            first, second = second, first
        elif self.bot.active_creature.speed == self.player.active_creature.speed:
            if random.random() < 0.5:
                first, second = second, first
                
        # Execute attacks
        for attacker, action in [(first, player_action if first == self.player else bot_action),
                               (second, bot_action if second == self.bot else player_action)]:
            if isinstance(action.thing, Creature):
                continue
                
            skill = action.thing
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
            
            # Force swap if creature fainted
            if defender.active_creature.hp == 0:
                available_creatures = [c for c in defender.creatures if c.hp > 0]
                if available_creatures:
                    creature_choices = [SelectThing(creature) for creature in available_creatures]
                    new_creature = self._wait_for_choice(defender, creature_choices).thing
                    defender.active_creature = new_creature

    def get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

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
