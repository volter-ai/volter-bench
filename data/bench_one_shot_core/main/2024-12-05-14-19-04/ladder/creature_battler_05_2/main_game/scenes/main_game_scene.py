from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
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
            if player_action is None:
                self._transition_to_scene("MainMenuScene")
                return
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if bot_action is None:
                self._transition_to_scene("MainMenuScene")
                return
                
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._transition_to_scene("MainMenuScene")
                return

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back to Menu")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button, back_button])
        
        if choice == back_button:
            return None
            
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            skill_choices.append(Button("Back"))
            skill_choice = self._wait_for_choice(player, skill_choices)
            
            if isinstance(skill_choice, Button):  # Back button
                return self.get_player_action(player)
            return ("attack", skill_choice.thing)
        else:
            # Show available creatures
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            if not available_creatures:
                return None
                
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            creature_choices.append(Button("Back"))
            creature_choice = self._wait_for_choice(player, creature_choices)
            
            if isinstance(creature_choice, Button):  # Back button
                return self.get_player_action(player)
            return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            
        # Determine attack order
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            first, second = (self.player, player_action), (self.bot, bot_action)
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            first, second = (self.bot, bot_action), (self.player, player_action)
        else:
            if random.random() < 0.5:
                first, second = (self.player, player_action), (self.bot, bot_action)
            else:
                first, second = (self.bot, bot_action), (self.player, player_action)
                
        # Execute attacks
        if first[1][0] == "attack":
            self.execute_attack(first[0], second[0], first[1][1])
        if second[1][0] == "attack" and second[0].active_creature.hp > 0:
            self.execute_attack(second[0], first[0], second[1][1])

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"It dealt {final_damage} damage!")

    def get_type_multiplier(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def check_battle_end(self):
        # Check if either player has any creatures left
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        # Force swap if active creature is fainted
        if self.player.active_creature.hp == 0:
            available = [c for c in self.player.creatures if c.hp > 0]
            if available:
                creature_choices = [SelectThing(creature) for creature in available]
                choice = self._wait_for_choice(self.player, creature_choices)
                self.player.active_creature = choice.thing
                
        if self.bot.active_creature.hp == 0:
            available = [c for c in self.bot.creatures if c.hp > 0]
            if available:
                self.bot.active_creature = random.choice(available)
                
        return False
