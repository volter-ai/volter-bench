from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP" 
            for c in self.player.creatures
        )
        bot_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP"
            for c in self.bot.creatures
        )
        
        return f"""=== Battle Scene ===
Your Team:
{player_creatures_status}
Active: {self.player.active_creature.display_name}

Opponent's Team: 
{bot_creatures_status}
Active: {self.bot.active_creature.display_name}

> Attack - Use a skill
> Swap - Switch active creature (if available)
"""

    def run(self):
        while True:
            # Check for knockouts and handle forced swaps
            if self.handle_knockouts():
                battle_result = self.check_battle_end()
                if battle_result is not None:
                    self.end_battle(battle_result)
                    return

            # Player Choice Phase
            player_action = self.get_turn_action(self.player)
            if player_action is None:
                self.end_battle(False)
                return

            # Foe Choice Phase
            bot_action = self.get_turn_action(self.bot)
            if bot_action is None:
                self.end_battle(True)
                return
            
            # Resolution Phase
            self.resolve_turn(player_action, bot_action)

            # Check battle end
            battle_result = self.check_battle_end()
            if battle_result is not None:
                self.end_battle(battle_result)
                return

    def end_battle(self, player_won: bool):
        """Handle end of battle cleanup and transition"""
        # Reset creature states
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

        # Show result and transition
        if player_won:
            self._show_text(self.player, "You won the battle!")
        else:
            self._show_text(self.player, "You lost the battle!")
        self._transition_to_scene("MainMenuScene")

    def handle_knockouts(self):
        """Handle forced swapping for knocked out creatures"""
        swaps_occurred = False
        
        for current_player in [self.player, self.bot]:
            if (current_player.active_creature.hp <= 0 and 
                any(c.hp > 0 for c in current_player.creatures if c != current_player.active_creature)):
                
                available_creatures = [
                    SelectThing(c) for c in current_player.creatures 
                    if c.hp > 0 and c != current_player.active_creature
                ]
                
                self._show_text(
                    current_player,
                    f"{current_player.active_creature.display_name} was knocked out! Choose a new creature!"
                )
                
                choice = self._wait_for_choice(current_player, available_creatures)
                current_player.active_creature = choice.thing
                swaps_occurred = True
                
        return swaps_occurred

    def get_turn_action(self, current_player):
        while True:
            # Main choice menu
            choices = []
            if current_player.active_creature.hp > 0:
                choices.append(Button("Attack"))
            
            available_creatures = self.get_available_creatures(current_player)
            if available_creatures:
                choices.append(Button("Swap"))
            
            if not choices:
                return None
                
            main_choice = self._wait_for_choice(current_player, choices)
            
            if isinstance(main_choice, Button) and main_choice.display_name == "Attack":
                # Show skills with Back option
                skill_choices = [
                    SelectThing(skill) 
                    for skill in current_player.active_creature.skills
                ]
                skill_choices.append(Button("Back"))
                
                choice = self._wait_for_choice(current_player, skill_choices)
                if isinstance(choice, Button):
                    continue
                return choice
                
            else:  # Swap
                # Show available creatures with Back option
                creature_choices = [
                    SelectThing(creature)
                    for creature in available_creatures
                ]
                creature_choices.append(Button("Back"))
                
                choice = self._wait_for_choice(current_player, creature_choices)
                if isinstance(choice, Button):
                    continue
                return choice

    def get_available_creatures(self, player):
        """Get list of creatures that can be swapped to"""
        return [
            creature for creature in player.creatures
            if creature != player.active_creature and creature.hp > 0
        ]

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
            self._show_text(self.player, f"Swapped to {player_action.thing.display_name}!")
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            self._show_text(self.player, f"Opponent swapped to {bot_action.thing.display_name}!")
            
        # Determine order for skill execution
        if self.bot.active_creature.speed == self.player.active_creature.speed:
            # Random order on speed tie
            if random.random() < 0.5:
                first, second = self.player, self.bot
            else:
                first, second = self.bot, self.player
        elif self.bot.active_creature.speed > self.player.active_creature.speed:
            first, second = self.bot, self.player
        else:
            first, second = self.player, self.bot
            
        # Execute skills
        if not isinstance(first.active_creature, Creature):
            self.execute_skill(first, second, player_action if first == self.player else bot_action)
        if not isinstance(second.active_creature, Creature):
            self.execute_skill(second, first, bot_action if second == self.bot else player_action)

    def execute_skill(self, attacker, defender, action):
        if not isinstance(action.thing, Creature):  # It's a skill
            skill = action.thing
            target = defender.active_creature
            
            # Calculate damage
            if skill.is_physical:
                raw_damage = (
                    attacker.active_creature.attack + 
                    skill.base_damage - 
                    target.defense
                )
            else:
                raw_damage = (
                    skill.base_damage * 
                    attacker.active_creature.sp_attack / 
                    target.sp_defense
                )
                
            # Apply type effectiveness
            multiplier = self.get_type_multiplier(skill.skill_type, target.creature_type)
            final_damage = int(raw_damage * multiplier)
            
            # Apply damage
            target.hp = max(0, target.hp - final_damage)
            
            effectiveness_text = ""
            if multiplier > 1:
                effectiveness_text = " It's super effective!"
            elif multiplier < 1:
                effectiveness_text = " It's not very effective..."
            
            self._show_text(
                attacker,
                f"{attacker.active_creature.display_name} used {skill.display_name}! "
                f"Dealt {final_damage} damage!{effectiveness_text}"
            )

    def get_type_multiplier(self, skill_type, target_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(target_type, 1.0)

    def check_battle_end(self):
        """Returns True if player won, False if bot won, None if battle continues"""
        player_has_active = any(c.hp > 0 for c in self.player.creatures)
        bot_has_active = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_active:
            return False
        elif not bot_has_active:
            return True
            
        return None
