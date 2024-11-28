from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
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
            # Check for battle end before each turn
            if self.check_battle_end():
                self._quit_whole_game()  # Properly end the game when battle is over
                return
                
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)

    def get_available_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def get_player_action(self, player):
        available_creatures = self.get_available_creatures(player)
        
        # If active creature is knocked out, force a swap if possible
        if player.active_creature.hp <= 0:
            if available_creatures:
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                self._show_text(player, f"{player.active_creature.display_name} was knocked out! Choose a new creature!")
                return self._wait_for_choice(player, creature_choices)
            else:
                # No available creatures means battle should end
                return Button("No Action")  # This will be caught by check_battle_end
        
        # Normal turn choices
        choices = [Button("Attack")]
        if available_creatures:
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
        # Skip if either action is "No Action" (due to no available creatures)
        if isinstance(player_action, Button) or isinstance(bot_action, Button):
            return
            
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            
        # Then handle attacks
        first_player, second_player = self.determine_turn_order()
        first_action = player_action if first_player == self.player else bot_action
        second_action = bot_action if first_player == self.player else player_action
        
        if isinstance(first_action.thing, Skill):
            self.execute_skill(first_player, first_action.thing)
        if isinstance(second_action.thing, Skill):
            self.execute_skill(second_player, second_action.thing)

    def determine_turn_order(self):
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return self.player, self.bot
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return self.bot, self.player
        else:
            return random.choice([(self.player, self.bot), (self.bot, self.player)])

    def execute_skill(self, attacker, skill):
        if attacker == self.player:
            defender = self.bot
        else:
            defender = self.player
            
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

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

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
