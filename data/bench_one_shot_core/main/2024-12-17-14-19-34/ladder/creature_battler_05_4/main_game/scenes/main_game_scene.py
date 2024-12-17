from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.reset_creatures()

    def reset_creatures(self):
        # Reset all creatures to full HP
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

Available actions:
> Attack
{"> Swap" if self.get_available_creatures(self.player) else ""}"""

    def run(self):
        while True:
            # Handle knocked out creatures first
            if self.player.active_creature.hp <= 0:
                if not self.force_swap(self.player):
                    self.end_battle()
                    return
            if self.bot.active_creature.hp <= 0:
                if not self.force_swap(self.bot):
                    self.end_battle()
                    return

            # Get and resolve actions
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self.end_battle()
                return

    def end_battle(self):
        """Handle end of battle and transition back to main menu"""
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        winner = "You win!" if player_has_creatures else "You lose!"
        self._show_text(self.player, winner)
        
        # Give player a moment to see the result
        continue_button = Button("Continue")
        self._wait_for_choice(self.player, [continue_button])
        
        # Return to main menu
        self._transition_to_scene("MainMenuScene")

    def get_available_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def force_swap(self, player):
        available = [c for c in player.creatures if c.hp > 0]
        if not available:
            return False
        
        creature_choices = [SelectThing(creature) for creature in available]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        return True

    def get_player_action(self, player):
        choices = []
        
        # Always add Attack option if creature has skills
        if player.active_creature.skills:
            choices.append(Button("Attack"))
        
        # Only add Swap if there are creatures to swap to
        if self.get_available_creatures(player):
            choices.append(Button("Swap"))
        
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            return self._wait_for_choice(player, skill_choices)
        else:
            available_creatures = self.get_available_creatures(player)
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            return self._wait_for_choice(player, creature_choices)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing

        # Then handle attacks
        first, second = self.determine_order(player_action, bot_action)
        self.execute_action(first)
        if isinstance(second.thing, Skill):  # Only execute second attack if it's a skill (not a swap)
            self.execute_action(second)

    def determine_order(self, player_action, bot_action):
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_action, bot_action
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return bot_action, player_action
        else:
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def execute_action(self, action):
        if isinstance(action.thing, Creature):
            return  # Swap already handled
            
        skill = action.thing
        attacker = self.player if action.thing in self.player.active_creature.skills else self.bot
        defender = self.bot if attacker == self.player else self.player
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)

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
        
        return not player_has_creatures or not bot_has_creatures
