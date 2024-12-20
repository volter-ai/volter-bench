from typing import Dict, List, Optional, Tuple
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Player, Creature, Skill

TYPE_EFFECTIVENESS = {
    "fire": {"leaf": 2.0, "water": 0.5},
    "water": {"fire": 2.0, "leaf": 0.5},
    "leaf": {"water": 2.0, "fire": 0.5},
    "normal": {}
}

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self._reset_creatures()

    def _reset_creatures(self):
        """Reset all creatures to starting state"""
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        
        return f"""=== Battle Scene ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {opponent_creature.display_name}: HP {opponent_creature.hp}/{opponent_creature.max_hp}

> Attack
> Swap
"""

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = TYPE_EFFECTIVENESS.get(skill.skill_type, {}).get(defender.creature_type, 1.0)
        final_damage = int(raw_damage * effectiveness)
        return max(1, final_damage)  # Minimum 1 damage

    def _get_available_creatures(self, player: Player) -> List[Creature]:
        return [c for c in player.creatures if c != player.active_creature and c.hp > 0]

    def _handle_knocked_out(self, player: Player) -> bool:
        """Returns True if player can continue, False if they're defeated"""
        if player.active_creature.hp <= 0:
            available = self._get_available_creatures(player)
            if not available:
                return False
            
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            
        return True

    def _get_player_action(self, player: Player) -> Tuple[str, Optional[Skill | Creature]]:
        """Get player's action for the turn"""
        while True:
            # Main action menu
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(player, [attack_button, swap_button])

            if choice == attack_button:
                # Attack submenu with Back option
                skill_choices = [SelectThing(s) for s in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skill_choices + [back_button])
                
                if skill_choice == back_button:
                    continue  # Return to main menu
                return ("attack", skill_choice.thing)
            
            else:  # Swap chosen
                available = self._get_available_creatures(player)
                if available:
                    # Swap submenu with Back option
                    creature_choices = [SelectThing(c) for c in available]
                    back_button = Button("Back")
                    creature_choice = self._wait_for_choice(player, creature_choices + [back_button])
                    
                    if creature_choice == back_button:
                        continue  # Return to main menu
                    return ("swap", creature_choice.thing)
                # If no creatures available to swap, default to using first skill
                return ("attack", player.active_creature.skills[0])

    def _execute_turn(self, first_player: Player, second_player: Player, 
                     first_action: Tuple[str, Optional[Skill | Creature]], 
                     second_action: Tuple[str, Optional[Skill | Creature]]):
        """Execute a turn's worth of actions"""
        
        # Handle swaps first
        for player, action in [(first_player, first_action), (second_player, second_action)]:
            if action[0] == "swap":
                self._show_text(player, f"{player.active_creature.display_name} swaps out!")
                player.active_creature = action[1]
                self._show_text(player, f"{player.active_creature.display_name} swaps in!")

        # Then handle attacks
        for attacker, defender, action in [(first_player, second_player, first_action),
                                         (second_player, first_player, second_action)]:
            if action[0] == "attack":
                skill = action[1]
                damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
                defender.active_creature.hp -= damage
                self._show_text(attacker, 
                    f"{attacker.active_creature.display_name} uses {skill.display_name}! Deals {damage} damage!")

    def run(self):
        while True:
            # Player choice phase
            player_action = self._get_player_action(self.player)

            # Bot choice phase
            bot_creature = self.opponent.active_creature
            if bot_creature.hp < bot_creature.max_hp * 0.3:
                # Try to swap if low health
                available = self._get_available_creatures(self.opponent)
                if available:
                    bot_action = ("swap", available[0])
                else:
                    bot_action = ("attack", bot_creature.skills[0])
            else:
                bot_action = ("attack", bot_creature.skills[0])

            # Resolution phase
            if self.player.active_creature.speed >= self.opponent.active_creature.speed:
                self._execute_turn(self.player, self.opponent, player_action, bot_action)
            else:
                self._execute_turn(self.opponent, self.player, bot_action, player_action)

            # Check for knocked out creatures
            if not self._handle_knocked_out(self.player):
                self._show_text(self.player, "You lost the battle!")
                break
            if not self._handle_knocked_out(self.opponent):
                self._show_text(self.player, "You won the battle!")
                break

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")
