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
                # After battle ends, return to main menu
                self._transition_to_scene("MainMenuScene")
                return

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            skill_choices.append(back_button)
            skill_choice = self._wait_for_choice(player, skill_choices)
            
            if skill_choice == back_button:
                return None
            return {"type": "attack", "skill": skill_choice.thing}
            
        elif choice == swap_button:
            # Show available creatures
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            if not available_creatures:
                self._show_text(player, "No other creatures available!")
                return None
                
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            creature_choices.append(back_button)
            creature_choice = self._wait_for_choice(player, creature_choices)
            
            if creature_choice == back_button:
                return None
            return {"type": "swap", "creature": creature_choice.thing}

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"Go {self.player.active_creature.display_name}!")
            
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            self._show_text(self.player, f"Foe sent out {self.bot.active_creature.display_name}!")

        # Then handle attacks
        first = self.player
        second = self.bot
        first_action = player_action
        second_action = bot_action
        
        if bot_action["type"] == "attack" and player_action["type"] == "attack":
            if self.bot.active_creature.speed > self.player.active_creature.speed:
                first = self.bot
                second = self.player
                first_action = bot_action
                second_action = player_action
            elif self.bot.active_creature.speed == self.player.active_creature.speed:
                if random.random() < 0.5:
                    first = self.bot
                    second = self.player
                    first_action = bot_action
                    second_action = player_action

        if first_action["type"] == "attack":
            self.execute_attack(first, second, first_action["skill"])
            
        if second.active_creature.hp > 0 and second_action["type"] == "attack":
            self.execute_attack(second, first, second_action["skill"])

        self.handle_fainted_creatures()

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}!")

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_fainted_creatures(self):
        for player in [self.player, self.bot]:
            if player.active_creature.hp <= 0:
                self._show_text(self.player, f"{player.active_creature.display_name} fainted!")
                
                # Get available creatures
                available = [c for c in player.creatures if c.hp > 0]
                if not available:
                    return
                    
                if player == self.bot:
                    player.active_creature = available[0]
                    self._show_text(self.player, f"Foe sent out {player.active_creature.display_name}!")
                else:
                    creature_choices = [SelectThing(creature) for creature in available]
                    choice = self._wait_for_choice(player, creature_choices)
                    player.active_creature = choice.thing
                    self._show_text(self.player, f"Go {player.active_creature.display_name}!")

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
