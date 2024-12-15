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
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

> Attack - Use a skill
> Swap - Switch active creature
"""

    def run(self):
        while True:
            # Get player action
            player_action = self.get_player_action(self.player)
            if not player_action:
                return
                
            # Get bot action
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                return
                
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._transition_to_scene("MainMenuScene")
                return

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
                    creature for creature in player.creatures 
                    if creature != player.active_creature and creature.hp > 0
                ]
                
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                creatures = [SelectThing(creature) for creature in available_creatures]
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, creatures + [back_button])
                
                if creature_choice == back_button:
                    continue
                    
                return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"You switched to {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Foe switched to {bot_action[1].display_name}!")

        # Then handle attacks
        first = self.player
        first_action = player_action
        second = self.bot
        second_action = bot_action

        if bot_action[0] == "attack" and player_action[0] == "attack":
            if self.bot.active_creature.speed > self.player.active_creature.speed:
                first = self.bot
                first_action = bot_action
                second = self.player
                second_action = player_action
            elif self.bot.active_creature.speed == self.player.active_creature.speed:
                if random.random() < 0.5:
                    first = self.bot
                    first_action = bot_action
                    second = self.player
                    second_action = player_action

        if first_action[0] == "attack":
            self.execute_attack(first, second, first_action[1])
            
        if second.active_creature.hp > 0 and second_action[0] == "attack":
            self.execute_attack(second, first, second_action[1])

    def execute_attack(self, attacker, defender, skill):
        # Calculate raw damage
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
            
        # Handle fainting
        if defender.active_creature.hp <= 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} was knocked out!")
            self.handle_fainted_creature(defender)

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)

    def handle_fainted_creature(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if not available_creatures:
            return
            
        self._show_text(player, "Choose next creature:")
        creatures = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, creatures)
        player.active_creature = choice.thing
        self._show_text(self.player, f"{'You' if player == self.player else 'Foe'} sent out {choice.thing.display_name}!")

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
