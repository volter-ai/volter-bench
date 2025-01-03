from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
from dataclasses import dataclass
from typing import Optional, Union
import random

@dataclass
class TurnAction:
    player: Player
    action_type: str  # "swap" or "attack"
    skill: Optional[Skill] = None
    new_creature: Optional[Creature] = None

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self._initialize_creatures()

    def _initialize_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

> Attack
> Swap"""

    def _get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        return int(raw_damage * multiplier)

    def _get_player_action(self, player: Player) -> TurnAction:
        while True:
            # Main menu
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(player, [attack_button, swap_button])

            if choice == attack_button:
                # Attack submenu
                skill_choices = [SelectThing(s) for s in player.active_creature.skills]
                back_button = Button("Back")
                skill_choices.append(back_button)
                
                skill_choice = self._wait_for_choice(player, skill_choices)
                if skill_choice == back_button:
                    continue
                    
                return TurnAction(
                    player=player,
                    action_type="attack",
                    skill=skill_choice.thing
                )
            else:  # Swap submenu
                available_creatures = [c for c in player.creatures 
                                    if c.hp > 0 and c != player.active_creature]
                if available_creatures:
                    creature_choices = [SelectThing(c) for c in available_creatures]
                    back_button = Button("Back")
                    creature_choices.append(back_button)
                    
                    creature_choice = self._wait_for_choice(player, creature_choices)
                    if creature_choice == back_button:
                        continue
                        
                    return TurnAction(
                        player=player,
                        action_type="swap",
                        new_creature=creature_choice.thing
                    )
                else:
                    self._show_text(player, "No other creatures available to swap to!")
                    continue

    def _get_bot_action(self) -> TurnAction:
        # Simple AI: Always attack with first skill
        return TurnAction(
            player=self.bot,
            action_type="attack",
            skill=self.bot.active_creature.skills[0]
        )

    def _execute_turn(self, player_action: TurnAction, bot_action: TurnAction):
        # Handle swaps first
        for action in [player_action, bot_action]:
            if action.action_type == "swap":
                action.player.active_creature = action.new_creature
                self._show_text(self.player, 
                    f"{action.player.display_name} swapped to {action.new_creature.display_name}!")

        # Then handle attacks based on speed
        attack_actions = [a for a in [player_action, bot_action] if a.action_type == "attack"]
        if len(attack_actions) == 2:
            # Determine order based on speed with random tiebreaker
            player_speed = self.player.active_creature.speed
            bot_speed = self.bot.active_creature.speed
            
            if player_speed > bot_speed:
                attack_order = attack_actions
            elif player_speed < bot_speed:
                attack_order = list(reversed(attack_actions))
            else:  # Equal speed - random order
                attack_order = attack_actions if random.random() < 0.5 else list(reversed(attack_actions))
        else:
            attack_order = attack_actions

        # Execute attacks
        for action in attack_order:
            if action.player == self.player:
                defender = self.bot
            else:
                defender = self.player
                
            damage = self._calculate_damage(
                action.player.active_creature, 
                defender.active_creature, 
                action.skill
            )
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            
            self._show_text(self.player, 
                f"{action.player.active_creature.display_name} used {action.skill.display_name}! "
                f"Dealt {damage} damage to {defender.active_creature.display_name}!")

    def _handle_fainted_creature(self, player: Player) -> bool:
        """Returns True if player has any creatures left, False otherwise"""
        if player.active_creature.hp > 0:
            return True
            
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return False
            
        self._show_text(self.player, f"{player.active_creature.display_name} fainted!")
        choices = [SelectThing(c) for c in available_creatures]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return True

    def run(self):
        while True:
            # Player Choice Phase
            player_action = self._get_player_action(self.player)
            
            # Foe Choice Phase
            bot_action = self._get_bot_action()
            
            # Resolution Phase
            self._execute_turn(player_action, bot_action)

            # Check for fainted creatures
            player_has_creatures = self._handle_fainted_creature(self.player)
            bot_has_creatures = self._handle_fainted_creature(self.bot)

            if not player_has_creatures:
                self._show_text(self.player, "You lost!")
                break
            elif not bot_has_creatures:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")
