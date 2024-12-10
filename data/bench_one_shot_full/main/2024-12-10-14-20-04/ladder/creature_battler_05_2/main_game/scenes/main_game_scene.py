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
        return f"""=== Battle Scene ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Enemy {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

Your Actions:
> Attack
> Swap
"""

    def run(self):
        while True:
            # Player phase
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue
                
            # Bot phase
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                continue

            # Resolution phase
            self.resolve_actions(
                (self.player, player_action),
                (self.bot, bot_action)
            )
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self.handle_attack_choice(player)
        elif choice == swap_button:
            return self.handle_swap_choice(player)

    def handle_attack_choice(self, player):
        back_button = Button("Back")
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return None
            
        return ("attack", choice.thing)

    def handle_swap_choice(self, player):
        back_button = Button("Back")
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        
        if not available_creatures:
            return None
            
        choices = [SelectThing(creature) for creature in available_creatures]
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return None
            
        return ("swap", choice.thing)

    def resolve_actions(self, player_tuple, bot_tuple):
        # Handle swaps first
        if player_tuple[1][0] == "swap":
            self.player.active_creature = player_tuple[1][1]
        if bot_tuple[1][0] == "swap":
            self.bot.active_creature = bot_tuple[1][1]

        # Then handle attacks
        first, second = self.get_action_order(player_tuple, bot_tuple)
        self.execute_action(*first)
        self.execute_action(*second)

    def get_action_order(self, player_tuple, bot_tuple):
        if player_tuple[1][0] == "swap" or bot_tuple[1][0] == "swap":
            return player_tuple, bot_tuple
            
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_tuple, bot_tuple
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return bot_tuple, player_tuple
        else:
            return random.choice([(player_tuple, bot_tuple), (bot_tuple, player_tuple)])

    def execute_action(self, actor, action):
        if action[0] == "attack":
            skill = action[1]
            attacker = actor
            defender = self.bot if actor == self.player else self.player
            
            damage = self.calculate_damage(skill, attacker.active_creature, defender.active_creature)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)

    def calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

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
