from dataclasses import dataclass
from typing import Union, Optional
import random
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button, DictionaryChoice

@dataclass
class Action:
    type: str  # "skill" or "swap"
    player: "Player"
    skill: Optional["Skill"] = None
    swap_to: Optional["Creature"] = None

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
        # Reset creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

Your Team:
{self.format_team(self.player)}

Foe's Team:
{self.format_team(self.bot)}"""

    def format_team(self, player):
        return "\n".join(f"- {c.display_name}: {c.hp}/{c.max_hp} HP" for c in player.creatures)

    def run(self):
        while True:
            # Player Choice Phase
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue

            # Foe Choice Phase
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                continue

            # Resolution Phase
            self.resolve_turn(player_action, bot_action)
            
            # Handle knocked out creatures
            if not self.handle_knocked_out_creatures():
                # Battle is over, return to main menu
                self._transition_to_scene("MainMenuScene")
                return

    def get_player_action(self, player) -> Optional[Action]:
        while True:
            attack = Button("Attack")
            swap = Button("Swap")
            choices = [attack, swap]
            
            choice = self._wait_for_choice(player, choices)
            
            if choice == attack:
                skill_action = self.get_skill_choice(player)
                if skill_action:
                    return skill_action
            else:
                swap_action = self.get_swap_choice(player)
                if swap_action:
                    return swap_action

    def get_skill_choice(self, player) -> Optional[Action]:
        back = Button("Back")
        choices = [Button(skill.display_name) for skill in player.active_creature.skills]
        choices.append(back)
        
        choice = self._wait_for_choice(player, choices)
        
        if choice == back:
            return None
            
        selected_skill = player.active_creature.skills[choices.index(choice)]
        return Action(type="skill", player=player, skill=selected_skill)

    def get_swap_choice(self, player) -> Optional[Action]:
        back = Button("Back")
        valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        choices = [SelectThing(creature) for creature in valid_creatures]
        choices.append(back)
        
        choice = self._wait_for_choice(player, choices)
        
        if choice == back:
            return None
            
        selected_creature = choice.thing
        return Action(type="swap", player=player, swap_to=selected_creature)

    def resolve_turn(self, player_action: Action, bot_action: Action):
        # Handle swaps first
        actions = [player_action, bot_action]
        swap_actions = [a for a in actions if a.type == "swap"]
        skill_actions = [a for a in actions if a.type == "skill"]
        
        # Execute swaps
        for action in swap_actions:
            self._show_text(action.player, f"{action.player.active_creature.display_name} swaps out!")
            action.player.active_creature = action.swap_to
            self._show_text(action.player, f"{action.swap_to.display_name} swaps in!")

        # Execute skills in speed order
        if not skill_actions:
            return  # If no skills were used (both players swapped), we're done
        elif len(skill_actions) == 1:
            # Only one skill was used
            self.execute_skill(skill_actions[0].player, skill_actions[0].skill)
        else:
            # Both used skills - check speed
            first = skill_actions[0]
            second = skill_actions[1]
            if second.player.active_creature.speed > first.player.active_creature.speed:
                first, second = second, first
            elif second.player.active_creature.speed == first.player.active_creature.speed:
                # Random tiebreak
                if random.random() < 0.5:
                    first, second = second, first
            
            self.execute_skill(first.player, first.skill)
            self.execute_skill(second.player, second.skill)

    def execute_skill(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         defender.active_creature.defense)
        else:
            raw_damage = (attacker.active_creature.sp_attack / 
                         defender.active_creature.sp_defense * 
                         skill.base_damage)

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, 
                                            defender.active_creature.creature_type)
        
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.active_creature.hp = max(0, 
                                        defender.active_creature.hp - final_damage)
        
        # Show result
        effectiveness = ""
        if multiplier > 1:
            effectiveness = "It's super effective!"
        elif multiplier < 1:
            effectiveness = "It's not very effective..."
            
        self._show_text(attacker, 
                       f"{attacker.active_creature.display_name} used {skill.display_name}! {effectiveness}")

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knocked_out_creatures(self) -> bool:
        """Returns False if battle should end, True if it can continue"""
        for player in [self.player, self.bot]:
            if player.active_creature.hp <= 0:
                self._show_text(player, 
                              f"{player.active_creature.display_name} was knocked out!")
                
                # Check for available creatures
                valid_creatures = [c for c in player.creatures if c.hp > 0]
                if not valid_creatures:
                    winner = self.bot if player == self.player else self.player
                    self._show_text(self.player,
                                  f"{winner.display_name} wins the battle!")
                    return False
                    
                # Force swap
                choices = [SelectThing(creature) for creature in valid_creatures]
                choice = self._wait_for_choice(player, choices)
                player.active_creature = choice.thing
                self._show_text(player,
                              f"{player.display_name} sends out {choice.thing.display_name}!")
                
        return True
