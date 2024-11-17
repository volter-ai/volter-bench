from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.reset_creatures()

    def reset_creatures(self):
        # Reset all creatures to max HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

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
                break

        self.reset_creatures()

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            choices = [SelectThing(skill) for skill in player.active_creature.skills]
            choices.append(back_button)
            choice = self._wait_for_choice(player, choices)
            if choice == back_button:
                return None
            return ("attack", choice.thing)
            
        elif choice == swap_button:
            available_creatures = [c for c in player.creatures 
                                if c != player.active_creature and c.hp > 0]
            if not available_creatures:
                self._show_text(player, "No other creatures available!")
                return None
                
            choices = [SelectThing(creature) for creature in available_creatures]
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
            self._show_text(self.bot, f"Foe sends out {bot_action[1].display_name}!")

        # Then handle attacks
        if player_action[0] == "attack" and bot_action[0] == "attack":
            # Determine order based on speed
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                first, second = (self.player, player_action[1]), (self.bot, bot_action[1])
            elif self.player.active_creature.speed < self.bot.active_creature.speed:
                first, second = (self.bot, bot_action[1]), (self.player, player_action[1])
            else:
                if random.random() < 0.5:
                    first, second = (self.player, player_action[1]), (self.bot, bot_action[1])
                else:
                    first, second = (self.bot, bot_action[1]), (self.player, player_action[1])
                    
            self.execute_attack(first[0], first[1])
            if self.bot.active_creature.hp > 0 and self.player.active_creature.hp > 0:
                self.execute_attack(second[0], second[1])

    def execute_attack(self, attacker, skill):
        if attacker == self.player:
            attacking_creature = self.player.active_creature
            defending_creature = self.bot.active_creature
        else:
            attacking_creature = self.bot.active_creature
            defending_creature = self.player.active_creature

        # Calculate damage
        if skill.is_physical:
            raw_damage = attacking_creature.attack + skill.base_damage - defending_creature.defense
        else:
            raw_damage = (attacking_creature.sp_attack / defending_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defending_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defending_creature.hp = max(0, defending_creature.hp - final_damage)
        
        self._show_text(attacker, 
            f"{attacking_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage!")

        if defending_creature.hp <= 0:
            self.handle_knockout(defending_creature.display_name)

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def handle_knockout(self, creature_name):
        self._show_text(self.player, f"{creature_name} was knocked out!")
        
        # Force swap if any creatures remain
        for player in [self.player, self.bot]:
            if player.active_creature.hp <= 0:
                available = [c for c in player.creatures if c.hp > 0]
                if available:
                    choices = [SelectThing(c) for c in available]
                    choice = self._wait_for_choice(player, choices)
                    player.active_creature = choice.thing
                    self._show_text(player, f"Go {choice.thing.display_name}!")

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
