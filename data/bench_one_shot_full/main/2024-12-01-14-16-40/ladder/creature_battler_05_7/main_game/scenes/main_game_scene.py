from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
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

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.bot.display_name}'s {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap"""

    def run(self):
        while True:
            # Check for battle end before each turn
            if self.check_battle_end():
                self._quit_whole_game()
                
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)

    def get_player_action(self, player):
        while True:  # Main menu loop
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            main_choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if main_choice == attack_button:
                # Attack submenu
                choices = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                choices.append(back_button)
                
                sub_choice = self._wait_for_choice(player, choices)
                if sub_choice == back_button:
                    continue  # Go back to main menu
                return sub_choice
                
            else:  # Swap choice
                # Get valid creatures for swapping
                valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                
                if not valid_creatures:
                    self._show_text(player, "No creatures to swap to! Must attack!")
                    continue  # Go back to main menu
                
                choices = [SelectThing(creature) for creature in valid_creatures]
                back_button = Button("Back")
                choices.append(back_button)
                
                sub_choice = self._wait_for_choice(player, choices)
                if sub_choice == back_button:
                    continue  # Go back to main menu
                return sub_choice

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
                
            defender = self.bot if attacker == self.player else self.player
            self.execute_skill(attacker.active_creature, defender.active_creature, action.thing)
            
            # Handle KO
            if defender.active_creature.hp <= 0:
                valid_creatures = [c for c in defender.creatures if c.hp > 0]
                if valid_creatures:
                    choices = [SelectThing(creature) for creature in valid_creatures]
                    swap = self._wait_for_choice(defender, choices)
                    defender.active_creature = swap.thing

    def execute_skill(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        # Final damage
        final_damage = int(raw_damage * effectiveness)
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"Dealt {final_damage} damage!")

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_map = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        
        return effectiveness_map.get((skill_type, defender_type), 1.0)

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won!")
            return True
            
        return False
