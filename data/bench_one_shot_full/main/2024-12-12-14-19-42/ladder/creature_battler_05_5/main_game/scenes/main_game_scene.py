from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
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
                return
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                return
                
            # Resolve actions
            self.resolve_turn(
                (self.player, player_action), 
                (self.bot, bot_action)
            )
            
            # Check for battle end
            if self.check_battle_end():
                return

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self.handle_attack_choice(player)
        else:
            return self.handle_swap_choice(player)

    def handle_attack_choice(self, player):
        skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, skill_choices + [back_button])
        
        if choice == back_button:
            return self.get_player_action(player)
        
        return {"type": "attack", "skill": choice.thing}

    def handle_swap_choice(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not available_creatures:
            return self.get_player_action(player)
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, creature_choices + [back_button])
        
        if choice == back_button:
            return self.get_player_action(player)
            
        return {"type": "swap", "creature": choice.thing}

    def resolve_turn(self, player_with_action, bot_with_action):
        player, player_action = player_with_action
        bot, bot_action = bot_with_action

        # Handle swaps first
        if player_action["type"] == "swap":
            player.active_creature = player_action["creature"]
            self._show_text(player, f"Go {player_action['creature'].display_name}!")
            
        if bot_action["type"] == "swap":
            bot.active_creature = bot_action["creature"]
            self._show_text(player, f"Foe sent out {bot_action['creature'].display_name}!")

        # Handle attacks
        if player_action["type"] == "attack" and bot_action["type"] == "attack":
            first, first_action, second, second_action = self.determine_turn_order(
                (player, player_action),
                (bot, bot_action)
            )
            self.execute_attack(first, first_action, second)
            if second.active_creature.hp > 0:
                self.execute_attack(second, second_action, first)

    def determine_turn_order(self, player1_with_action, player2_with_action):
        player1, action1 = player1_with_action
        player2, action2 = player2_with_action
        
        speed1 = player1.active_creature.speed
        speed2 = player2.active_creature.speed
        
        if speed1 > speed2:
            return player1, action1, player2, action2
        elif speed2 > speed1:
            return player2, action2, player1, action1
        else:
            if random.random() < 0.5:
                return player1, action1, player2, action2
            else:
                return player2, action2, player1, action1

    def execute_attack(self, attacker, action, defender):
        skill = action["skill"]
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {damage} damage!")

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

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
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        if not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene") 
            return True
            
        return False
