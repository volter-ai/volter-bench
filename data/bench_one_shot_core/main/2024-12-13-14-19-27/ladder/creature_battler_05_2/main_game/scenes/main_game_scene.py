from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Reset creature stats
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

> Attack
> Swap (if you have other creatures available)
"""

    def run(self):
        while True:
            # Check for battle end before each turn
            if self.check_battle_end():
                self._quit_whole_game()  # Properly end the game when battle is over
                return
                
            # Handle forced swaps if needed
            if self.player.active_creature.hp <= 0:
                self.handle_forced_swap(self.player)
            if self.bot.active_creature.hp <= 0:
                self.handle_forced_swap(self.bot)
                
            # Get actions
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)

    def get_available_swap_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def get_player_action(self, player):
        choices = [Button("Attack")]
        
        # Only add swap option if there are creatures to swap to
        available_creatures = self.get_available_swap_creatures(player)
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

    def handle_forced_swap(self, player):
        available = [c for c in player.creatures if c.hp > 0]
        if available:
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, type(self.player.creatures[0])):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, type(self.bot.creatures[0])):
            self.bot.active_creature = bot_action.thing
            
        # Then handle attacks
        if isinstance(player_action.thing, type(self.player.active_creature.skills[0])):
            if self.player.active_creature.speed >= self.bot.active_creature.speed:
                self.execute_skill(player_action.thing, self.player.active_creature, self.bot.active_creature)
                if isinstance(bot_action.thing, type(self.bot.active_creature.skills[0])):
                    self.execute_skill(bot_action.thing, self.bot.active_creature, self.player.active_creature)
            else:
                if isinstance(bot_action.thing, type(self.bot.active_creature.skills[0])):
                    self.execute_skill(bot_action.thing, self.bot.active_creature, self.player.active_creature)
                self.execute_skill(player_action.thing, self.player.active_creature, self.bot.active_creature)

    def execute_skill(self, skill, attacker, defender):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! Dealt {final_damage} damage!")

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        # Check if either player has any creatures left
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won!")
            return True
            
        return False
