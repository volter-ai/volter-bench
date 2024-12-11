from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        for p in [self.player, self.bot]:
            p.active_creature = p.creatures[0]
            for c in p.creatures:
                c.hp = c.max_hp

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

Your Team:
{self._format_team(self.player)}

Foe's Team:
{self._format_team(self.bot)}
"""

    def _format_team(self, player):
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" for c in player.creatures])

    def _get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == defender_type:
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        return int(raw_damage * multiplier)

    def _handle_knocked_out(self, player):
        available = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not available:
            return False
            
        choices = [SelectThing(c) for c in available]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return True

    def _get_player_action(self, player) -> tuple[bool, any]:
        while True:
            # Main choice
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Attack submenu
                skill_choices = [SelectThing(s) for s in player.active_creature.skills]
                back_button = Button("Back")
                choice = self._wait_for_choice(player, skill_choices + [back_button])
                
                if choice == back_button:
                    continue
                return False, choice.thing
                
            else:  # Swap
                # Swap submenu
                available = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                if available:
                    swap_choices = [SelectThing(c) for c in available]
                    back_button = Button("Back")
                    choice = self._wait_for_choice(player, swap_choices + [back_button])
                    
                    if choice == back_button:
                        continue
                    return True, choice.thing
                else:
                    self._show_text(player, "No creatures available to swap!")
                    continue

    def _execute_turn(self, first_player, first_action, second_player, second_action):
        for player, (is_swap, action) in [(first_player, first_action), (second_player, second_action)]:
            if is_swap:  # Swap action
                self._show_text(self.player, 
                    f"{player.display_name} swapped to {action.display_name}!")
                player.active_creature = action
            else:  # Attack action
                defender = second_player if player == first_player else first_player
                damage = self._calculate_damage(player.active_creature, defender.active_creature, action)
                defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
                
                self._show_text(self.player, 
                    f"{player.active_creature.display_name} used {action.display_name}! "
                    f"Dealt {damage} damage to {defender.active_creature.display_name}!")
                
                if defender.active_creature.hp == 0:
                    if not self._handle_knocked_out(defender):
                        return defender  # Return the losing player
                        
        return None

    def run(self):
        while True:
            # Player Choice Phase
            player_action = self._get_player_action(self.player)
            
            # Foe Choice Phase
            bot_action = self._get_player_action(self.bot)
            
            # Determine turn order - swaps always go first
            if player_action[0]:  # Player is swapping
                first_player, first_action = self.player, player_action
                second_player, second_action = self.bot, bot_action
            elif bot_action[0]:  # Bot is swapping
                first_player, first_action = self.bot, bot_action
                second_player, second_action = self.player, player_action
            else:  # Both are attacks, use speed
                if self.player.active_creature.speed > self.bot.active_creature.speed:
                    first_player, first_action = self.player, player_action
                    second_player, second_action = self.bot, bot_action
                elif self.player.active_creature.speed < self.bot.active_creature.speed:
                    first_player, first_action = self.bot, bot_action
                    second_player, second_action = self.player, player_action
                else:  # Equal speed, random
                    if random.random() < 0.5:
                        first_player, first_action = self.player, player_action
                        second_player, second_action = self.bot, bot_action
                    else:
                        first_player, first_action = self.bot, bot_action
                        second_player, second_action = self.player, player_action
            
            # Execute turn and check for game end
            loser = self._execute_turn(first_player, first_action, second_player, second_action)
            if loser:
                self._show_text(self.player, 
                    "You won!" if loser == self.bot else "You lost!")
                self._transition_to_scene("MainMenuScene")
