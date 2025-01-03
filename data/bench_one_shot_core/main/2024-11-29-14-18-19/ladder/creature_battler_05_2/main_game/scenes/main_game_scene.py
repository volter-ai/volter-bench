from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
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
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                self._quit_whole_game()
                return
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                self._quit_whole_game()
                return

            # Resolve actions
            self.resolve_turn(
                (self.player, player_action),
                (self.bot, bot_action)
            )

            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()
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
        choices = skill_choices + [back_button]
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self.get_player_action(player)
        return {"type": "attack", "skill": choice.thing}

    def handle_swap_choice(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not available_creatures:
            return None
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices = creature_choices + [back_button]
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self.get_player_action(player)
        return {"type": "swap", "creature": choice.thing}

    def resolve_turn(self, player_data, bot_data):
        player, player_action = player_data
        bot, bot_action = bot_data

        # Handle swaps first
        if player_action["type"] == "swap":
            player.active_creature = player_action["creature"]
        if bot_action["type"] == "swap":
            bot.active_creature = bot_action["creature"]

        # Then handle attacks
        if player_action["type"] == "attack" and bot_action["type"] == "attack":
            first_data, second_data = self.determine_order(
                (player, player_action),
                (bot, bot_action)
            )
            self.execute_attack(first_data, second_data)
            if second_data[0].active_creature.hp > 0:
                self.execute_attack(second_data, first_data)

    def determine_order(self, player1_data, player2_data):
        player1, _ = player1_data
        player2, _ = player2_data
        
        speed1 = player1.active_creature.speed
        speed2 = player2.active_creature.speed
        
        if speed1 > speed2:
            return player1_data, player2_data
        elif speed2 > speed1:
            return player2_data, player1_data
        else:
            return random.choice([(player1_data, player2_data), (player2_data, player1_data)])

    def execute_attack(self, attacker_data, defender_data):
        attacker, action = attacker_data
        defender, _ = defender_data
        
        skill = action["skill"]
        target = defender.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - target.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / target.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, target.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        target.hp = max(0, target.hp - final_damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{target.display_name} took {final_damage} damage!")

    def get_type_multiplier(self, skill_type, target_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(target_type, 1.0)

    def check_battle_end(self):
        def has_available_creatures(player):
            return any(c.hp > 0 for c in player.creatures)

        if not has_available_creatures(self.player):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not has_available_creatures(self.bot):
            self._show_text(self.player, "You won the battle!")
            return True
            
        # Force swap if active creature is fainted
        for player in [self.player, self.bot]:
            if player.active_creature.hp <= 0:
                available = [c for c in player.creatures if c.hp > 0]
                if available:
                    choices = [SelectThing(c) for c in available]
                    choice = self._wait_for_choice(player, choices)
                    player.active_creature = choice.thing
                    
        return False
