from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature

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
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

Available actions:
> Attack
{"> Swap" if self.get_available_creatures(self.player) else ""}
"""

    def run(self):
        while True:
            # Check if forced swap needed
            if self.player.active_creature.hp <= 0:
                if not self.handle_forced_swap(self.player):
                    if self.check_battle_end():
                        self._transition_to_scene("MainMenuScene")
                        return
            if self.bot.active_creature.hp <= 0:
                if not self.handle_forced_swap(self.bot):
                    if self.check_battle_end():
                        self._transition_to_scene("MainMenuScene")
                        return

            # Get actions
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._transition_to_scene("MainMenuScene")
                return

    def get_available_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_forced_swap(self, player):
        available = self.get_available_creatures(player)
        if not available:
            return False
            
        self._show_text(self.player, f"{player.active_creature.display_name} was knocked out!")
        creature_choices = [SelectThing(creature) for creature in available]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        self._show_text(self.player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        return True

    def get_player_action(self, player):
        choices = []
        
        # Always offer attack
        attack_button = Button("Attack")
        choices.append(attack_button)
        
        # Only offer swap if valid swaps exist
        available = self.get_available_creatures(player)
        if available:
            swap_button = Button("Swap")
            choices.append(swap_button)
        
        choice = self._wait_for_choice(player, choices)
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            return self._wait_for_choice(player, skill_choices)
        else:
            # Show available creatures
            creature_choices = [SelectThing(creature) for creature in available]
            return self._wait_for_choice(player, creature_choices)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
            self._show_text(self.player, f"{self.player.display_name} swapped to {player_action.thing.display_name}!")
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            self._show_text(self.player, f"{self.bot.display_name} swapped to {bot_action.thing.display_name}!")
            
        # Then handle attacks
        first, second = self.get_action_order(player_action, bot_action)
        self.execute_action(first)
        
        # Only execute second action if both creatures still alive
        if self.player.active_creature.hp > 0 and self.bot.active_creature.hp > 0:
            self.execute_action(second)

    def get_action_order(self, player_action, bot_action):
        player_speed = self.player.active_creature.speed
        bot_speed = self.bot.active_creature.speed
        
        if player_speed > bot_speed:
            return player_action, bot_action
        elif bot_speed > player_speed:
            return bot_action, player_action
        else:
            import random
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def execute_action(self, action):
        if isinstance(action.thing, Creature):
            return  # Swap already handled
            
        skill = action.thing
        attacker = self.player.active_creature if action in self.player.active_creature.skills else self.bot.active_creature
        defender = self.bot.active_creature if attacker == self.player.active_creature else self.player.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = max(1, int(raw_damage * multiplier))  # Minimum 1 damage
        
        defender.hp = max(0, defender.hp - final_damage)
        
        # Show damage text
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"Dealt {final_damage} damage!")

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
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
