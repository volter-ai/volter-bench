from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Player, Creature
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
Enemy {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

Available actions:
> Attack (if you have skills)
> Swap (if you have other creatures)
"""

    def run(self):
        try:
            while True:
                # Player turn
                player_action = self.get_player_action(self.player)
                if not player_action:
                    # No valid actions means this player has lost
                    self._show_text(self.player, "You have no valid moves!")
                    self._show_text(self.player, "You lost!")
                    self._transition_to_scene("MainMenuScene")
                    return
                    
                bot_action = self.get_player_action(self.bot)
                if not bot_action:
                    # No valid actions means the bot has lost
                    self._show_text(self.player, "The opponent has no valid moves!")
                    self._show_text(self.player, "You won!")
                    self._transition_to_scene("MainMenuScene")
                    return
                
                # Execute actions
                self.resolve_turn(player_action, bot_action)
                
                # Check for battle end
                if self.check_battle_end():
                    self._transition_to_scene("MainMenuScene")
                    return
        except RandomModeGracefulExit:
            # Even in random mode exit, we should transition
            self._transition_to_scene("MainMenuScene")
            raise

    def get_player_action(self, player: Player):
        available_choices = []
        
        # Check if Attack is valid
        if player.active_creature and player.active_creature.skills:
            available_choices.append(Button("Attack"))
            
        # Check if Swap is valid
        valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if valid_creatures:
            available_choices.append(Button("Swap"))
            
        # If no choices available, return None to indicate no valid moves
        if not available_choices:
            return None
            
        choice = self._wait_for_choice(player, available_choices)
        
        if choice.display_name == "Attack":
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            return self._wait_for_choice(player, skill_choices)
        else:  # Swap
            creature_choices = [SelectThing(creature) for creature in valid_creatures]
            return self._wait_for_choice(player, creature_choices)

    def resolve_turn(self, player_action, bot_action):
        # Determine order
        first_action, second_action = self.determine_action_order(player_action, bot_action)
        
        # Execute actions
        self.execute_action(first_action)
        self.execute_action(second_action)

    def determine_action_order(self, player_action, bot_action):
        # Swaps go first
        if isinstance(player_action.thing, Creature) and not isinstance(bot_action.thing, Creature):
            return player_action, bot_action
        elif isinstance(bot_action.thing, Creature) and not isinstance(player_action.thing, Creature):
            return bot_action, player_action
            
        # Compare speeds for attacks
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_action, bot_action
        elif self.bot.active_creature.speed > self.player.active_creature.speed:
            return bot_action, player_action
        else:
            if random.random() < 0.5:
                return player_action, bot_action
            return bot_action, player_action

    def execute_action(self, action):
        if isinstance(action.thing, Creature):
            if action.thing in self.player.creatures:
                self.player.active_creature = action.thing
            else:
                self.bot.active_creature = action.thing
        else:  # Skill
            self.execute_skill(action.thing, self.player if action.thing in self.player.active_creature.skills else self.bot)

    def execute_skill(self, skill, attacker):
        defender = self.bot if attacker == self.player else self.player
        
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Force swap if creature fainted
        if defender.active_creature.hp == 0:
            valid_creatures = [c for c in defender.creatures if c.hp > 0]
            if valid_creatures:
                choices = [SelectThing(creature) for creature in valid_creatures]
                swap_choice = self._wait_for_choice(defender, choices)
                defender.active_creature = swap_choice.thing

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
            self._show_text(self.player, "You lost!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won!")
            return True
            
        return False
