from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.reset_creatures()
        
    def reset_creatures(self):
        # Reset all creatures to full HP
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

    def __str__(self):
        p1 = self.player
        p2 = self.bot
        return f"""=== Battle ===
{p1.display_name}'s {p1.active_creature.display_name}: {p1.active_creature.hp}/{p1.active_creature.max_hp} HP
{p2.display_name}'s {p2.active_creature.display_name}: {p2.active_creature.hp}/{p2.active_creature.max_hp} HP

> Attack
> Swap"""

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": effectiveness = 2.0
            elif defender.creature_type == "water": effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": effectiveness = 2.0
            elif defender.creature_type == "leaf": effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": effectiveness = 2.0
            elif defender.creature_type == "fire": effectiveness = 0.5
            
        return int(raw_damage * effectiveness)

    def get_available_creatures(self, player: Player) -> list[Creature]:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_knocked_out(self, player: Player) -> bool:
        if player.active_creature.hp <= 0:
            available = self.get_available_creatures(player)
            if not available:
                return False
            
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            
        return True

    def execute_turn(self, first_player: Player, first_action: tuple, second_player: Player, second_action: tuple):
        for current_player, action in [(first_player, first_action), (second_player, second_action)]:
            other_player = second_player if current_player == first_player else first_player
            
            action_type, action_target = action
            if action_type == "swap":
                current_player.active_creature = action_target
                self._show_text(current_player, f"{current_player.display_name} swapped to {action_target.display_name}!")
            else: # attack
                damage = self.calculate_damage(current_player.active_creature, other_player.active_creature, action_target)
                other_player.active_creature.hp -= damage
                self._show_text(current_player, 
                    f"{current_player.active_creature.display_name} used {action_target.display_name} for {damage} damage!")
                
                if not self.handle_knocked_out(other_player):
                    self._show_text(self.player, 
                        "You win!" if other_player == self.bot else "You lose!")
                    return False
                    
        return True

    def get_player_action(self, player: Player) -> tuple:
        while True:
            choice = self._wait_for_choice(player, [Button("Attack"), Button("Swap")])
            
            if isinstance(choice, Button) and choice.display_name == "Attack":
                skill_choices = [SelectThing(s) for s in player.active_creature.skills]
                skill_choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skill_choices)
                
                if isinstance(skill_choice, SelectThing):
                    return ("attack", skill_choice.thing)
                    
            else: # Swap
                creature_choices = [SelectThing(c) for c in self.get_available_creatures(player)]
                creature_choices.append(Button("Back"))
                creature_choice = self._wait_for_choice(player, creature_choices)
                
                if isinstance(creature_choice, SelectThing):
                    return ("swap", creature_choice.thing)

    def run(self):
        while True:
            # Get actions
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Determine order
            if player_action[0] == "swap" or bot_action[0] == "swap":
                # Swaps always go first
                if player_action[0] == "swap":
                    first, second = self.player, self.bot
                    first_action, second_action = player_action, bot_action
                else:
                    first, second = self.bot, self.player
                    first_action, second_action = bot_action, player_action
            else:
                # Speed determines order for attacks
                if self.player.active_creature.speed > self.bot.active_creature.speed:
                    first, second = self.player, self.bot
                    first_action, second_action = player_action, bot_action
                elif self.player.active_creature.speed < self.bot.active_creature.speed:
                    first, second = self.bot, self.player
                    first_action, second_action = bot_action, player_action
                else:
                    # Random on speed tie
                    if random.random() < 0.5:
                        first, second = self.player, self.bot
                        first_action, second_action = player_action, bot_action
                    else:
                        first, second = self.bot, self.player
                        first_action, second_action = bot_action, player_action
                        
            # Execute turn
            if not self.execute_turn(first, first_action, second, second_action):
                break
                
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")
