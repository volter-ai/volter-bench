from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, create_from_game_database
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self._reset_creatures()

    def _reset_creatures(self):
        # Reset all creatures to max HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

Your choices:
> Attack
> Swap"""

    def _get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == defender_type or skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        return int(raw_damage * multiplier)

    def _handle_player_turn(self, player: Player) -> tuple[str, any]:
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            while True:
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skill_choices + [back_button])
                
                if skill_choice == back_button:
                    return self._handle_player_turn(player)
                return "attack", skill_choice.thing
                
        elif choice == swap_button:
            while True:
                available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, creature_choices + [back_button])
                
                if creature_choice == back_button:
                    return self._handle_player_turn(player)
                return "swap", creature_choice.thing

    def _execute_turn(self, player_action, bot_action):
        player = self.player
        bot = self.bot
        
        # Handle swaps first
        if player_action[0] == "swap":
            player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            bot.active_creature = bot_action[1]
            
        # Then handle attacks
        if player_action[0] == "attack" and bot_action[0] == "attack":
            # Determine order based on speed
            if player.active_creature.speed > bot.active_creature.speed or \
               (player.active_creature.speed == bot.active_creature.speed and random.random() < 0.5):
                first, second = (player, player_action[1]), (bot, bot_action[1])
            else:
                first, second = (bot, bot_action[1]), (player, player_action[1])
                
            # Execute attacks in order
            for attacker, skill in [first, second]:
                if attacker == player:
                    defender = bot
                else:
                    defender = player
                    
                damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
                defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
                
                self._show_text(player, f"{attacker.active_creature.display_name} used {skill.display_name}!")
                self._show_text(player, f"It dealt {damage} damage!")
                
                if defender.active_creature.hp == 0:
                    break

    def _handle_knocked_out(self, player: Player) -> bool:
        if player.active_creature.hp > 0:
            return False
            
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return True
            
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        return False

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Get actions
            player_action = self._handle_player_turn(self.player)
            bot_action = self._handle_player_turn(self.bot)
            
            # Execute turn
            self._execute_turn(player_action, bot_action)
            
            # Check for knocked out creatures
            player_lost = self._handle_knocked_out(self.player)
            bot_lost = self._handle_knocked_out(self.bot)
            
            if player_lost or bot_lost:
                if player_lost:
                    self._show_text(self.player, "You lost!")
                else:
                    self._show_text(self.player, "You won!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return
