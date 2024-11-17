from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                continue
                
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._transition_to_scene("MainMenuScene")

    def get_player_action(self, player: Player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Show skills with Back option
                back_button = Button("Back")
                choices = [SelectThing(skill) for skill in player.active_creature.skills]
                choices.append(back_button)
                
                skill_choice = self._wait_for_choice(player, choices)
                if skill_choice == back_button:
                    continue  # Go back to main menu
                return skill_choice
                
            else:  # Swap chosen
                valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                if not valid_creatures:
                    return None
                    
                # Show creatures with Back option
                back_button = Button("Back")
                choices = [SelectThing(c) for c in valid_creatures]
                choices.append(back_button)
                
                creature_choice = self._wait_for_choice(player, choices)
                if creature_choice == back_button:
                    continue  # Go back to main menu
                return creature_choice

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            
        # Then handle attacks
        first, second = self.get_action_order(player_action, bot_action)
        self.execute_action(first)
        self.execute_action(second)

    def get_action_order(self, player_action, bot_action):
        if isinstance(player_action.thing, Creature) or isinstance(bot_action.thing, Creature):
            return player_action, bot_action
            
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_action, bot_action
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return bot_action, player_action
        else:
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def execute_action(self, action):
        if isinstance(action.thing, Creature):
            return
            
        skill = action.thing
        attacker = self.player.active_creature if action in self.player.active_creature.skills else self.bot.active_creature
        defender = self.bot.active_creature if action in self.player.active_creature.skills else self.player.active_creature
        
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

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won!")
            return True
            
        if self.player.active_creature.hp == 0:
            valid_creatures = [c for c in self.player.creatures if c.hp > 0]
            if valid_creatures:
                choices = [SelectThing(c) for c in valid_creatures]
                choice = self._wait_for_choice(self.player, choices)
                self.player.active_creature = choice.thing
                
        if self.bot.active_creature.hp == 0:
            valid_creatures = [c for c in self.bot.creatures if c.hp > 0]
            if valid_creatures:
                choices = [SelectThing(c) for c in valid_creatures]
                choice = self._wait_for_choice(self.bot, choices)
                self.bot.active_creature = choice.thing
                
        return False
