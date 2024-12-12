from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
> Swap (if you have other creatures available)
"""

    def run(self):
        while True:
            # Handle forced swaps if active creatures are knocked out
            if self.player.active_creature.hp <= 0:
                if not self.handle_forced_swap(self.player):
                    self._show_text(self.player, "You lost!")
                    self._quit_whole_game()
                    return
            if self.bot.active_creature.hp <= 0:
                if not self.handle_forced_swap(self.bot):
                    self._show_text(self.player, "You won!")
                    self._quit_whole_game()
                    return

            # Player turn
            self.current_player_action = self.get_player_action(self.player)
            self.current_bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(self.current_player_action, self.current_bot_action)

    def get_valid_swap_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_forced_swap(self, player):
        valid_creatures = self.get_valid_swap_creatures(player)
        if not valid_creatures:
            return False
            
        self._show_text(self.player, f"{player.active_creature.display_name} was knocked out!")
        choices = [SelectThing(creature) for creature in valid_creatures]
        swap_choice = self._wait_for_choice(player, choices)
        player.active_creature = swap_choice.thing
        self._show_text(self.player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        return True

    def get_player_action(self, player):
        choices = []
        
        # Only add Attack if creature is alive
        if player.active_creature.hp > 0:
            choices.append(Button("Attack"))
            
        # Only add Swap if there are valid creatures to swap to
        if self.get_valid_swap_creatures(player):
            choices.append(Button("Swap"))
            
        if not choices:
            # This should never happen due to forced swap handling
            raise Exception("No valid actions available")
            
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            choices = [SelectThing(skill) for skill in player.active_creature.skills]
            return self._wait_for_choice(player, choices)
        else:  # Swap
            valid_creatures = self.get_valid_swap_creatures(player)
            choices = [SelectThing(creature) for creature in valid_creatures]
            return self._wait_for_choice(player, choices)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, type(self.player.creatures[0])):
            self.player.active_creature = player_action.thing
            self._show_text(self.player, f"You switched to {player_action.thing.display_name}!")
        if isinstance(bot_action.thing, type(self.bot.creatures[0])):
            self.bot.active_creature = bot_action.thing
            self._show_text(self.player, f"Foe switched to {bot_action.thing.display_name}!")
            
        # Then handle attacks
        first, second = self.get_action_order(player_action, bot_action)
        self.execute_action(first)
        self.execute_action(second)

    def get_action_order(self, player_action, bot_action):
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_action, bot_action
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return bot_action, player_action
        else:
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def execute_action(self, action):
        if isinstance(action.thing, type(self.player.creatures[0])):
            return  # Skip if it was a swap
            
        skill = action.thing
        attacker = self.player.active_creature if action == self.current_player_action else self.bot.active_creature
        defender = self.bot.active_creature if action == self.current_player_action else self.player.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * multiplier)
        
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
