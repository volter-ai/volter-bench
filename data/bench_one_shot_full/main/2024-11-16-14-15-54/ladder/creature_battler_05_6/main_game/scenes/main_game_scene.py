from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Reset creature HP
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

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
                break

    def get_player_action(self, player):
        action_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [action_button, swap_button])
        
        if choice == action_button:
            return self.get_skill_choice(player)
        else:
            return self.get_swap_choice(player)

    def get_skill_choice(self, player):
        creature = player.active_creature
        choices = [SelectThing(skill) for skill in creature.skills]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return None
            
        return ("attack", choice.thing)

    def get_swap_choice(self, player):
        valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not valid_creatures:
            self._show_text(player, "No creatures available to swap!")
            return None
            
        choices = [SelectThing(creature) for creature in valid_creatures]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return None
            
        return ("swap", choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"Go {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Foe sends out {bot_action[1].display_name}!")

        # Then handle attacks
        if player_action[0] == "attack" and bot_action[0] == "attack":
            # Determine order
            first = self.player if self.player.active_creature.speed > self.bot.active_creature.speed else self.bot
            second = self.bot if first == self.player else self.player
            first_action = player_action if first == self.player else bot_action
            second_action = bot_action if first == self.player else player_action
            
            self.execute_attack(first, second, first_action[1])
            if second.active_creature.hp > 0:
                self.execute_attack(second, first, second_action[1])

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        raw_damage = self.calculate_raw_damage(attacker.active_creature, defender.active_creature, skill)
        type_factor = self.get_type_factor(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * type_factor)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} fainted!")
            self.handle_fainted_creature(defender)

    def calculate_raw_damage(self, attacker, defender, skill):
        if skill.is_physical:
            return attacker.attack + skill.base_damage - defender.defense
        else:
            return (attacker.sp_attack / defender.sp_defense) * skill.base_damage

    def get_type_factor(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def handle_fainted_creature(self, player):
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        if not valid_creatures:
            return
            
        choices = [SelectThing(creature) for creature in valid_creatures]
        self._show_text(player, "Choose next creature!")
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        self._show_text(self.player, f"Go {choice.thing.display_name}!")

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
