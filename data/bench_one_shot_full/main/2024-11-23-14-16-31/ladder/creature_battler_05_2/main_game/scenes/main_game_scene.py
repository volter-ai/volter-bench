from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        
        player_creatures_status = "\n".join(
            f"- {c.display_name}: {c.hp}/{c.max_hp} HP" 
            for c in self.player.creatures
        )
        
        return f"""=== Battle ===
Your Active Creature:
{player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP

Opponent's Creature:
{opponent_creature.display_name}: {opponent_creature.hp}/{opponent_creature.max_hp} HP

Your Team:
{player_creatures_status}

> Attack
> Swap"""

    def run(self):
        while True:
            # Check if forced swap needed
            if self.player.active_creature.hp <= 0:
                if not self.handle_forced_swap(self.player):
                    self.end_battle("You lost the battle!")
                    return
                    
            if self.opponent.active_creature.hp <= 0:
                if not self.handle_forced_swap(self.opponent):
                    self.end_battle("You won the battle!")
                    return

            # Normal turn
            player_action = self.get_player_action(self.player)
            if player_action is None:  # Player chose "Back" at top level
                continue
                
            opponent_action = self.get_player_action(self.opponent)
            
            # Execute actions in speed order
            self.resolve_actions(player_action, opponent_action)

    def handle_forced_swap(self, player):
        """Handle forced swap when active creature is knocked out"""
        available = self.get_available_creatures(player)
        if not available:
            return False
            
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        
        if len(available) == 1:
            player.active_creature = available[0]
            self._show_text(player, f"Sending out {player.active_creature.display_name}!")
        else:
            choice = self._wait_for_choice(player, [
                SelectThing(creature) for creature in available
            ])
            player.active_creature = choice.thing
            self._show_text(player, f"Sending out {player.active_creature.display_name}!")
        return True

    def get_available_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def get_player_action(self, player):
        while True:
            # Top level choices
            choices = [Button("Attack"), Button("Swap"), Button("Back")]
            choice = self._wait_for_choice(player, choices)
            
            if isinstance(choice, Button) and choice.display_name == "Back":
                return None
                
            if isinstance(choice, Button) and choice.display_name == "Attack":
                # Show skills with back option
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(Button("Back"))
                
                skill_choice = self._wait_for_choice(player, skill_choices)
                if isinstance(skill_choice, Button):
                    continue
                return skill_choice
                
            else:  # Swap
                # Show available creatures with back option
                available = self.get_available_creatures(player)
                if not available:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                creature_choices = [SelectThing(creature) for creature in available]
                creature_choices.append(Button("Back"))
                
                creature_choice = self._wait_for_choice(player, creature_choices)
                if isinstance(creature_choice, Button):
                    continue
                return creature_choice

    def resolve_actions(self, player_action, opponent_action):
        # Determine order based on speed with random tiebreaker
        player_speed = self.player.active_creature.speed
        opponent_speed = self.opponent.active_creature.speed
        
        if player_speed == opponent_speed:
            if random.random() < 0.5:
                player_speed += 0.1  # Small boost to break tie
                
        if player_speed > opponent_speed:
            first, second = player_action, opponent_action
            first_player, second_player = self.player, self.opponent
        else:
            first, second = opponent_action, player_action
            first_player, second_player = self.opponent, self.player
            
        # Execute actions
        self.execute_action(first, first_player)
        if second_player.active_creature.hp > 0:
            self.execute_action(second, second_player)

    def execute_action(self, action, player):
        if isinstance(action.thing, Creature):
            old_creature = player.active_creature
            player.active_creature = action.thing
            self._show_text(player, 
                f"Withdrew {old_creature.display_name} and sent out {action.thing.display_name}!")
        else:  # Skill
            skill = action.thing
            target = self.opponent if player == self.player else self.player
            damage = self.calculate_damage(skill, player.active_creature, target.active_creature)
            target.active_creature.hp = max(0, target.active_creature.hp - damage)
            
            self._show_text(player, 
                f"{player.active_creature.display_name} used {skill.display_name}!")
            self._show_text(player, 
                f"Dealt {damage} damage to {target.active_creature.display_name}!")

    def calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def end_battle(self, message):
        self._show_text(self.player, message)
        
        # Reset creature states
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
            
        self._transition_to_scene("MainMenuScene")
