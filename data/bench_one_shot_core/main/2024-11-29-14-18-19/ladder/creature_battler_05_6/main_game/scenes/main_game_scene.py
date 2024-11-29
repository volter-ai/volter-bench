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
            self.resolve_turn(
                (self.player, player_action),
                (self.bot, bot_action)
            )

            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()

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
                    
                return {"type": "attack", "skill": skill_choice.thing}

            elif choice == swap_button:
                available_creatures = [
                    SelectThing(creature) 
                    for creature in player.creatures 
                    if creature != player.active_creature and creature.hp > 0
                ]
                
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, available_creatures + [back_button])
                
                if creature_choice == back_button:
                    continue
                    
                return {"type": "swap", "creature": creature_choice.thing}

    def resolve_turn(self, player_tuple, bot_tuple):
        # Handle swaps first
        if player_tuple[1]["type"] == "swap":
            self.player.active_creature = player_tuple[1]["creature"]
            self._show_text(self.player, f"You switched to {player_tuple[1]['creature'].display_name}!")
            
        if bot_tuple[1]["type"] == "swap":
            self.bot.active_creature = bot_tuple[1]["creature"]
            self._show_text(self.player, f"Foe switched to {bot_tuple[1]['creature'].display_name}!")

        # Then handle attacks
        first, second = self.determine_turn_order(player_tuple, bot_tuple)
        self.execute_action(*first)
        self.execute_action(*second)

    def determine_turn_order(self, player_tuple, bot_tuple):
        if player_tuple[1]["type"] == "swap" or bot_tuple[1]["type"] == "swap":
            return player_tuple, bot_tuple
            
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_tuple, bot_tuple
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return bot_tuple, player_tuple
        else:
            if random.random() < 0.5:
                return player_tuple, bot_tuple
            return bot_tuple, player_tuple

    def execute_action(self, attacker, action):
        if action["type"] != "attack":
            return
            
        defender = self.bot if attacker == self.player else self.player
        skill = action["skill"]
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {damage} damage to {defender.active_creature.display_name}!")

        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} was knocked out!")
            self.handle_knockout(defender)

    def calculate_damage(self, attacker, defender, skill):
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

    def handle_knockout(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            winner = self.player if player == self.bot else self.bot
            self._show_text(self.player, 
                "You won!" if winner == self.player else "You lost!")
            return
            
        if player == self.player:
            choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
        else:
            player.active_creature = available_creatures[0]

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        return not player_alive or not bot_alive
