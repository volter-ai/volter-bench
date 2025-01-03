from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, create_from_game_database
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self._initialize_creatures()

    def _initialize_creatures(self):
        # Reset creatures to full HP
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
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP"""

    def run(self):
        while True:
            # Player turn
            player_action = self._handle_turn_choice(self.player)
            if not player_action:
                return
                
            # Bot turn
            bot_action = self._handle_turn_choice(self.bot)
            if not bot_action:
                return
                
            # Resolve actions
            self._resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                self._quit_whole_game()
                return

    def _handle_turn_choice(self, current_player):
        if current_player.active_creature.hp <= 0:
            if not self._handle_forced_swap(current_player):
                return None
                
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(current_player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self._handle_attack_choice(current_player)
        else:
            return self._handle_swap_choice(current_player)

    def _handle_attack_choice(self, current_player):
        skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(current_player, skill_choices + [back_button])
        
        if choice == back_button:
            return self._handle_turn_choice(current_player)
        return {"type": "attack", "skill": choice.thing}

    def _handle_swap_choice(self, current_player):
        available_creatures = [
            creature for creature in current_player.creatures 
            if creature != current_player.active_creature and creature.hp > 0
        ]
        
        if not available_creatures:
            self._show_text(current_player, "No creatures available to swap!")
            return self._handle_turn_choice(current_player)
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(current_player, creature_choices + [back_button])
        
        if choice == back_button:
            return self._handle_turn_choice(current_player)
        return {"type": "swap", "creature": choice.thing}

    def _handle_forced_swap(self, current_player):
        available_creatures = [c for c in current_player.creatures if c.hp > 0]
        if not available_creatures:
            return False
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(current_player, creature_choices)
        current_player.active_creature = choice.thing
        return True

    def _resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            
        # Then handle attacks
        if player_action["type"] == "attack" and bot_action["type"] == "attack":
            # Determine order based on speed
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                first, second = player_action, bot_action
                first_player, second_player = self.player, self.bot
            elif self.player.active_creature.speed < self.bot.active_creature.speed:
                first, second = bot_action, player_action
                first_player, second_player = self.bot, self.player
            else:
                # Random if speeds are equal
                if random.random() < 0.5:
                    first, second = player_action, bot_action
                    first_player, second_player = self.player, self.bot
                else:
                    first, second = bot_action, player_action
                    first_player, second_player = self.bot, self.player
                    
            self._execute_attack(first["skill"], first_player, second_player)
            if second_player.active_creature.hp > 0:
                self._execute_attack(second["skill"], second_player, first_player)

    def _execute_attack(self, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"It dealt {final_damage} damage!")

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

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
