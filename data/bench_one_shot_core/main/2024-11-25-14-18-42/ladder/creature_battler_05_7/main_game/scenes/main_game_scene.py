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
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

Your choices:
> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                self._transition_to_scene("MainMenuScene")
                return
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                self._transition_to_scene("MainMenuScene")
                return
                
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._transition_to_scene("MainMenuScene")
                return

    def get_player_action(self, player):
        if player.active_creature.hp <= 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if not available_creatures:
                return None
                
            self._show_text(player, f"{player.active_creature.display_name} is knocked out!")
            choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            return ("swap", choice.thing)
            
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")
        
        while True:
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                skill_choices = [SelectThing(s) for s in player.active_creature.skills]
                skill_choice = self._wait_for_choice(player, skill_choices + [back_button])
                if skill_choice != back_button:
                    return ("attack", skill_choice.thing)
                    
            elif choice == swap_button:
                available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                if available_creatures:
                    creature_choices = [SelectThing(c) for c in available_creatures]
                    creature_choice = self._wait_for_choice(player, creature_choices + [back_button])
                    if creature_choice != back_button:
                        return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"You sent out {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Foe sent out {bot_action[1].display_name}!")
            
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
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show message
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}!")

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        elif skill_type == "fire":
            if creature_type == "leaf":
                return 2.0
            elif creature_type == "water":
                return 0.5
        elif skill_type == "water":
            if creature_type == "fire":
                return 2.0
            elif creature_type == "leaf":
                return 0.5
        elif skill_type == "leaf":
            if creature_type == "water":
                return 2.0
            elif creature_type == "fire":
                return 0.5
        return 1.0

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
