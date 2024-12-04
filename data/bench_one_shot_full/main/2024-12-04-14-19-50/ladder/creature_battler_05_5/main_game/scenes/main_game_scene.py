from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.type_effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5},
            "normal": {}
        }

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap"""

    def run(self):
        # Initialize battle
        self._setup_battle()
        
        while True:
            # Check for battle end
            if self._check_battle_end():
                return
                
            # Player turn
            player_action = self._get_player_action(self.player)
            bot_action = self._get_player_action(self.bot)
            
            # Resolve actions
            self._resolve_actions(player_action, bot_action)

    def _setup_battle(self):
        # Reset creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def _get_player_action(self, player):
        # Only show swap if there are available creatures to swap to
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        choices = [Button("Attack")]
        if available_creatures:
            choices.append(Button("Swap"))
        
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            return self._get_attack_choice(player)
        else:
            return self._get_swap_choice(player)

    def _get_attack_choice(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        return ("attack", self._wait_for_choice(player, choices).thing)

    def _get_swap_choice(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not available_creatures:
            # If no creatures available, force an attack
            return self._get_attack_choice(player)
            
        choices = [SelectThing(creature) for creature in available_creatures]
        return ("swap", self._wait_for_choice(player, choices).thing)

    def _resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            
        # Then handle attacks
        actions = [(self.player, player_action), (self.bot, bot_action)]
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        for player, action in actions:
            if action[0] == "attack":
                target = self.bot if player == self.player else self.player
                self._execute_attack(player.active_creature, target.active_creature, action[1])
                
                if self._check_battle_end():
                    return

    def _execute_attack(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        effectiveness = self.type_effectiveness.get(skill.skill_type, {}).get(defender.creature_type, 1.0)
        final_damage = int(raw_damage * effectiveness)
        
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        if effectiveness > 1:
            self._show_text(self.player, "It's super effective!")
        elif effectiveness < 1:
            self._show_text(self.player, "It's not very effective...")

    def _check_battle_end(self):
        def has_available_creatures(player):
            return any(c.hp > 0 for c in player.creatures)
            
        if not has_available_creatures(self.player):
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        if not has_available_creatures(self.bot):
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        if self.player.active_creature.hp == 0:
            available = [c for c in self.player.creatures if c.hp > 0]
            choices = [SelectThing(c) for c in available]
            self.player.active_creature = self._wait_for_choice(self.player, choices).thing
            
        if self.bot.active_creature.hp == 0:
            available = [c for c in self.bot.creatures if c.hp > 0]
            self.bot.active_creature = random.choice(available)
            
        return False
