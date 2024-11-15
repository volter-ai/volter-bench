from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Store queued actions
        self.player_action = None
        self.bot_action = None

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

What will you do?
> Attack
> Swap"""

    def run(self):
        while True:
            # Reset actions at start of turn
            self.player_action = ("attack", self.player.active_creature.skills[0])  # Default to first skill
            self.bot_action = ("attack", self.bot.active_creature.skills[0])  # Default to first skill
            
            # Player turn
            if not self.handle_knocked_out(self.player):
                return
            if not self.handle_knocked_out(self.bot):
                return
                
            self.player_phase()
            self.bot_phase()
            self.resolution_phase()

    def player_phase(self):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choice = self._wait_for_choice(self.player, [attack_button, swap_button])

        if choice == attack_button:
            back_button = Button("Back")
            skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
            skill_choice = self._wait_for_choice(self.player, skill_choices + [back_button])
            
            if skill_choice != back_button:
                self.player_action = ("attack", skill_choice.thing)
                
        elif choice == swap_button:
            available_creatures = [c for c in self.player.creatures 
                                if c != self.player.active_creature and c.hp > 0]
            if available_creatures:
                back_button = Button("Back")
                creature_choices = [SelectThing(c) for c in available_creatures]
                creature_choice = self._wait_for_choice(self.player, creature_choices + [back_button])
                
                if creature_choice != back_button:
                    self.player_action = ("swap", creature_choice.thing)

    def bot_phase(self):
        # Simple bot AI - randomly choose between attack and swap
        if random.random() < 0.8:  # 80% chance to attack
            skill = random.choice(self.bot.active_creature.skills)
            self.bot_action = ("attack", skill)
        else:
            available_creatures = [c for c in self.bot.creatures 
                                if c != self.bot.active_creature and c.hp > 0]
            if available_creatures:
                creature = random.choice(available_creatures)
                self.bot_action = ("swap", creature)
            else:
                # If no creatures to swap to, default to attack
                skill = random.choice(self.bot.active_creature.skills)
                self.bot_action = ("attack", skill)

    def resolution_phase(self):
        # Handle swaps first
        if self.player_action and self.player_action[0] == "swap":
            self.player.active_creature = self.player_action[1]
        if self.bot_action and self.bot_action[0] == "swap":
            self.bot.active_creature = self.bot_action[1]

        # Then handle attacks
        if (self.player_action and self.player_action[0] == "attack" and 
            self.bot_action and self.bot_action[0] == "attack"):
            # Determine order based on speed
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                self.execute_attack(self.player, self.bot, self.player_action[1])
                self.execute_attack(self.bot, self.player, self.bot_action[1])
            elif self.player.active_creature.speed < self.bot.active_creature.speed:
                self.execute_attack(self.bot, self.player, self.bot_action[1])
                self.execute_attack(self.player, self.bot, self.player_action[1])
            else:
                if random.random() < 0.5:
                    self.execute_attack(self.player, self.bot, self.player_action[1])
                    self.execute_attack(self.bot, self.player, self.bot_action[1])
                else:
                    self.execute_attack(self.bot, self.player, self.bot_action[1])
                    self.execute_attack(self.player, self.bot, self.player_action[1])

    def execute_attack(self, attacker, defender, skill):
        if defender.active_creature.hp <= 0:
            return
            
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"It dealt {final_damage} damage!")

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def reset_creatures_state(self, player):
        """Reset all creatures for a player back to their starting state"""
        for creature in player.creatures:
            creature.hp = creature.max_hp

    def handle_knocked_out(self, player):
        if player.active_creature.hp <= 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if not available_creatures:
                winner = self.player if player == self.bot else self.bot
                self._show_text(self.player, f"{winner.display_name} wins!")
                
                # Reset both players' creatures before transitioning
                self.reset_creatures_state(self.player)
                self.reset_creatures_state(self.bot)
                
                self._transition_to_scene("MainMenuScene")
                return False
                
            creature_choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing
            
        return True
