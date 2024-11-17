from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
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

> Attack
> Swap
"""

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
                # Properly transition back to main menu after battle ends
                self._transition_to_scene("MainMenuScene")
                return

    def get_player_action(self, current_player):
        while True:
            choices = [
                Button("Attack"),
                Button("Swap")
            ]
            
            choice = self._wait_for_choice(current_player, choices)

            if choice.display_name == "Attack":
                skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
                skill_choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(current_player, skill_choices)
                
                if isinstance(skill_choice, Button):
                    continue
                    
                return {"type": "attack", "skill": skill_choice.thing}

            elif choice.display_name == "Swap":
                available_creatures = [
                    creature for creature in current_player.creatures 
                    if creature != current_player.active_creature and creature.hp > 0
                ]
                
                if not available_creatures:
                    self._show_text(current_player, "No other creatures available!")
                    continue
                    
                swap_choices = [SelectThing(creature) for creature in available_creatures]
                swap_choices.append(Button("Back"))
                swap_choice = self._wait_for_choice(current_player, swap_choices)
                
                if isinstance(swap_choice, Button):
                    continue
                    
                return {"type": "swap", "creature": swap_choice.thing}

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"You switched to {player_action['creature'].display_name}!")
            
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            self._show_text(self.player, f"Foe switched to {bot_action['creature'].display_name}!")

        # Then handle attacks
        if player_action["type"] == "attack" and bot_action["type"] == "attack":
            first, second = self.determine_turn_order(
                (self.player, player_action), 
                (self.bot, bot_action)
            )
            self.execute_attack(*first)
            if second[1]["type"] == "attack" and second[0].active_creature.hp > 0:
                self.execute_attack(*second)

    def determine_turn_order(self, action1, action2):
        player1, action1 = action1
        player2, action2 = action2
        
        speed1 = player1.active_creature.speed
        speed2 = player2.active_creature.speed
        
        if speed1 > speed2:
            return (player1, action1), (player2, action2)
        elif speed2 > speed1:
            return (player2, action2), (player1, action1)
        else:
            if random.random() < 0.5:
                return (player1, action1), (player2, action2)
            return (player2, action2), (player1, action1)

    def execute_attack(self, attacker, action):
        skill = action["skill"]
        defender = self.bot if attacker == self.player else self.player
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         defender.active_creature.defense)
        else:
            raw_damage = ((attacker.active_creature.sp_attack / 
                          defender.active_creature.sp_defense) * 
                         skill.base_damage)

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(
            skill.skill_type, 
            defender.active_creature.creature_type
        )
        
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)

        # Show attack message
        self._show_text(
            self.player,
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage!"
        )

        # Handle fainting
        if defender.active_creature.hp <= 0:
            self._show_text(
                self.player,
                f"{defender.active_creature.display_name} was knocked out!"
            )
            self.handle_faint(defender)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_faint(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if not available_creatures:
            return
            
        choices = [SelectThing(creature) for creature in available_creatures]
        self._show_text(player, "Choose next creature!")
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        self._show_text(self.player, f"Sent out {choice.thing.display_name}!")

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
