from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

TYPE_EFFECTIVENESS = {
    "fire": {"leaf": 2.0, "water": 0.5},
    "water": {"fire": 2.0, "leaf": 0.5},
    "leaf": {"water": 2.0, "fire": 0.5},
    "normal": {}
}

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creatures at start
        self._reset_player_creatures(self.player)
        self._reset_player_creatures(self.bot)
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def _reset_player_creatures(self, player):
        """Reset all creatures for a player to their starting state"""
        for creature in player.creatures:
            creature.hp = creature.max_hp
        player.active_creature = None

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
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                skills = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skills + [back_button])
                
                if skill_choice == back_button:
                    continue
                    
                return ("attack", skill_choice.thing)
                
            elif choice == swap_button:
                available_creatures = [
                    SelectThing(creature) 
                    for creature in player.creatures 
                    if creature != player.active_creature and creature.hp > 0
                ]
                
                if not available_creatures:
                    self._show_text(player, "No creatures available to swap!")
                    continue
                    
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, available_creatures + [back_button])
                
                if creature_choice == back_button:
                    continue
                    
                return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"You swapped to {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Foe swapped to {bot_action[1].display_name}!")

        # Then handle attacks
        if player_action[0] == "attack" and bot_action[0] == "attack":
            # Determine order
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                first, second = (self.player, player_action[1]), (self.bot, bot_action[1])
            elif self.player.active_creature.speed < self.bot.active_creature.speed:
                first, second = (self.bot, bot_action[1]), (self.player, player_action[1])
            else:
                if random.random() < 0.5:
                    first, second = (self.player, player_action[1]), (self.bot, bot_action[1])
                else:
                    first, second = (self.bot, bot_action[1]), (self.player, player_action[1])
            
            self.execute_attack(first[0], first[1])
            if self.bot.active_creature.hp > 0:
                self.execute_attack(second[0], second[1])

    def execute_attack(self, attacker, skill):
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
        effectiveness = TYPE_EFFECTIVENESS.get(skill.skill_type, {}).get(defender.active_creature.creature_type, 1.0)
        final_damage = int(raw_damage * effectiveness)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}!")
        
        if defender.active_creature.hp == 0:
            self.handle_knockout(defender)

    def handle_knockout(self, player):
        self._show_text(self.player, f"{player.active_creature.display_name} was knocked out!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            if player == self.player:
                choices = [SelectThing(c) for c in available_creatures]
                choice = self._wait_for_choice(player, choices)
                player.active_creature = choice.thing
            else:
                player.active_creature = available_creatures[0]
            
            self._show_text(self.player, f"{player.active_creature.display_name} was sent out!")

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            # Reset creatures before transitioning
            self._reset_player_creatures(self.player)
            self._reset_player_creatures(self.bot)
            self._transition_to_scene("MainMenuScene")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            # Reset creatures before transitioning
            self._reset_player_creatures(self.player)
            self._reset_player_creatures(self.bot)
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
