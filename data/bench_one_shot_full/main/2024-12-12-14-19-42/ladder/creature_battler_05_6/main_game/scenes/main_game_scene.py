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
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

> Attack
{"> Swap" if self.get_available_creatures(self.player) else ""}
"""

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def calculate_damage(self, attacker: Creature, defender: Creature, skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        return int(raw_damage * multiplier)

    def get_available_creatures(self, player: Player) -> list[Creature]:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_fainted(self, player: Player) -> bool:
        available = self.get_available_creatures(player)
        if not available:
            return False
            
        choices = [SelectThing(creature) for creature in available]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return True

    def get_player_action(self) -> tuple:
        while True:
            # Main menu choices
            choices = [Button("Attack")]
            available_creatures = self.get_available_creatures(self.player)
            if available_creatures:
                choices.append(Button("Swap"))
                
            choice = self._wait_for_choice(self.player, choices)
            
            if choice.display_name == "Attack":
                # Attack submenu
                skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                skill_choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                
                if skill_choice.display_name == "Back":
                    continue
                    
                return ("attack", skill_choice.thing)
            else:
                # Swap submenu
                creature_choices = [SelectThing(c) for c in available_creatures]
                creature_choices.append(Button("Back"))
                creature_choice = self._wait_for_choice(self.player, creature_choices)
                
                if creature_choice.display_name == "Back":
                    continue
                    
                return ("swap", creature_choice.thing)

    def run(self):
        while True:
            # Player turn with Back option support
            player_action = self.get_player_action()

            # Bot turn
            available_bot_creatures = self.get_available_creatures(self.bot)
            if random.random() < 0.8 or not available_bot_creatures:  # 80% chance to attack or must attack if no swaps
                bot_action = ("attack", random.choice(self.bot.active_creature.skills))
            else:
                bot_action = ("swap", random.choice(available_bot_creatures))

            # Resolution phase
            actions = [(self.player, player_action), (self.bot, bot_action)]
            
            # Handle swaps first
            for player, action in actions:
                if action[0] == "swap":
                    player.active_creature = action[1]
                    self._show_text(self.player, f"{player.display_name} swapped to {action[1].display_name}!")

            # Then handle attacks - sort by speed
            for player, action in sorted(actions, key=lambda x: x[0].active_creature.speed, reverse=True):
                if action[0] == "attack":
                    opponent = self.bot if player == self.player else self.player
                    damage = self.calculate_damage(player.active_creature, opponent.active_creature, action[1])
                    opponent.active_creature.hp = max(0, opponent.active_creature.hp - damage)
                    
                    self._show_text(self.player, 
                        f"{player.display_name}'s {player.active_creature.display_name} used {action[1].display_name}! "
                        f"Dealt {damage} damage!")

                    if opponent.active_creature.hp == 0:
                        self._show_text(self.player, 
                            f"{opponent.display_name}'s {opponent.active_creature.display_name} fainted!")
                        if not self.handle_fainted(opponent):
                            self._show_text(self.player, 
                                f"{player.display_name} wins!" if player == self.player else "You lose!")
                            self._quit_whole_game()
