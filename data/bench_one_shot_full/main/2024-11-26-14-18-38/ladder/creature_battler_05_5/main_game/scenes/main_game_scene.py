from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self._setup_players()

    def _setup_players(self):
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
            player_action = self._get_player_action(self.player)
            if not player_action:
                continue
                
            # Bot turn
            bot_action = self._get_player_action(self.bot)
            if not bot_action:
                continue

            # Resolve actions
            self._resolve_actions(player_action, bot_action)

            # Check for battle end
            if self._check_battle_end():
                self._quit_whole_game()

    def _get_player_action(self, player):
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
                    
                return ("swap", creature_choice.thing)

    def _resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]

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

            self._execute_attack(first[0], first[1])
            if self._check_battle_end():
                return
            self._execute_attack(second[0], second[1])

    def _execute_attack(self, attacker, skill):
        if attacker == self.player:
            defender = self.bot
        else:
            defender = self.player

        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)

        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}")

        # Force swap if creature fainted
        if defender.active_creature.hp == 0:
            available_creatures = [c for c in defender.creatures if c.hp > 0]
            if available_creatures:
                if defender == self.player:
                    choices = [SelectThing(c) for c in available_creatures]
                    choice = self._wait_for_choice(defender, choices)
                    defender.active_creature = choice.thing
                else:
                    defender.active_creature = random.choice(available_creatures)

    def _get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def _check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)

        if not player_has_creatures:
            self._show_text(self.player, "You lost!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won!")
            return True
            
        return False
