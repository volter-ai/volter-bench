from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
from typing import List, Tuple
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self._initialize_battle()

    def _initialize_battle(self):
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
Opponent's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap
"""

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def _get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal" or defender_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _execute_turn(self, player_action: Tuple[str, Skill | Creature], bot_action: Tuple[str, Skill | Creature]):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"You switched to {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Opponent switched to {bot_action[1].display_name}!")

        # Then handle attacks based on speed
        if player_action[0] == "attack" and bot_action[0] == "attack":
            first = self.player if self.player.active_creature.speed >= self.bot.active_creature.speed else self.bot
            second = self.bot if first == self.player else self.player
            first_action = player_action if first == self.player else bot_action
            second_action = bot_action if first == self.player else player_action
            
            # Execute first attack
            damage = self._calculate_damage(first.active_creature, second.active_creature, first_action[1])
            second.active_creature.hp = max(0, second.active_creature.hp - damage)
            self._show_text(self.player, f"{first.active_creature.display_name} used {first_action[1].display_name}!")
            self._show_text(self.player, f"It dealt {damage} damage!")
            
            # Execute second attack if target still conscious
            if second.active_creature.hp > 0:
                damage = self._calculate_damage(second.active_creature, first.active_creature, second_action[1])
                first.active_creature.hp = max(0, first.active_creature.hp - damage)
                self._show_text(self.player, f"{second.active_creature.display_name} used {second_action[1].display_name}!")
                self._show_text(self.player, f"It dealt {damage} damage!")

    def _get_available_creatures(self, player: Player) -> List[Creature]:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def _handle_fainted_creatures(self) -> bool:
        """Returns True if battle should continue, False if it's over"""
        for player in [self.player, self.bot]:
            if player.active_creature.hp <= 0:
                available = self._get_available_creatures(player)
                if not available:
                    winner = self.bot if player == self.player else self.player
                    self._show_text(self.player, f"{winner.display_name} wins!")
                    return False
                    
                if player == self.player:
                    self._show_text(self.player, f"Your {player.active_creature.display_name} fainted!")
                    player.active_creature = available[0]  # Auto-select first available creature
                    self._show_text(self.player, f"Go, {player.active_creature.display_name}!")
                else:
                    new_creature = random.choice(available)
                    player.active_creature = new_creature
                    self._show_text(self.player, f"Opponent's {new_creature.display_name} was sent out!")
                    
        return True

    def run(self):
        while True:
            # Player turn
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            # Only show swap button if there are creatures to swap to
            available_creatures = self._get_available_creatures(self.player)
            choices = [attack_button] + ([swap_button] if available_creatures else [])
            
            choice = self._wait_for_choice(self.player, choices)
            
            if choice == attack_button:
                skill_choices = [SelectThing(s) for s in self.player.active_creature.skills]
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                player_action = ("attack", skill_choice.thing)
            else:
                creature_choices = [SelectThing(c) for c in available_creatures]
                creature_choice = self._wait_for_choice(self.player, creature_choices)
                player_action = ("swap", creature_choice.thing)
                
            # Bot turn
            bot_available = self._get_available_creatures(self.bot)
            if bot_available and random.random() < 0.2:  # 20% chance to swap if possible
                bot_creature = random.choice(bot_available)
                bot_action = ("swap", bot_creature)
            else:
                bot_skill = random.choice(self.bot.active_creature.skills)
                bot_action = ("attack", bot_skill)
                
            # Execute turn and check for battle end
            self._execute_turn(player_action, bot_action)
            if not self._handle_fainted_creatures():
                self._transition_to_scene("MainMenuScene")
                return
