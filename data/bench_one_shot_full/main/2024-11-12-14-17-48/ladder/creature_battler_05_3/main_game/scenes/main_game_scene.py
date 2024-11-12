from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, create_from_game_database
from main_game.models import Player, Creature, Action, Skill
import random

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
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Enemy {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

Available actions:
> Attack
{"> Swap" if self.get_available_creatures(self.player) else ""}
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:  # No valid actions available
                break
                
            bot_action = self.get_player_action(self.bot)
            if not bot_action:  # No valid actions available
                break
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_available_creatures(self, player: Player) -> list[Creature]:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def get_player_action(self, player: Player) -> Action | None:
        choices = [Button("Attack")]
        available_creatures = self.get_available_creatures(player)
        
        if available_creatures:
            choices.append(Button("Swap"))
        
        if not player.active_creature.skills and not available_creatures:
            return None  # No valid actions possible
            
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            selected_thing = self._wait_for_choice(player, skill_choices).thing
        else:
            # Show available creatures
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            selected_thing = self._wait_for_choice(player, creature_choices).thing
            
        # Create action instance
        action_data = {
            "display_name": f"{player.display_name}'s action",
            "description": f"Action by {player.display_name}",
            "prototype_id": "battle_action",
            "player": player,
            "thing": selected_thing
        }
        return Action(**action_data)

    def resolve_turn(self, player_action: Action, bot_action: Action):
        # Determine order
        first_action, second_action = self.determine_action_order(player_action, bot_action)
        
        # Execute actions in order
        self.execute_action(first_action)
        if second_action.player.active_creature.hp > 0:  # Only execute second action if creature still alive
            self.execute_action(second_action)

    def determine_action_order(self, player_action: Action, bot_action: Action):
        # Swaps go first
        if isinstance(player_action.thing, Creature) and not isinstance(bot_action.thing, Creature):
            return player_action, bot_action
        elif isinstance(bot_action.thing, Creature) and not isinstance(player_action.thing, Creature):
            return bot_action, player_action
            
        # Compare speeds for attacks
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_action, bot_action
        elif self.bot.active_creature.speed > self.player.active_creature.speed:
            return bot_action, player_action
        else:
            # Random if speeds are equal
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def execute_action(self, action: Action):
        if isinstance(action.thing, Creature):
            # Handle swap
            if action.player == self.player:
                self.player.active_creature = action.thing
            else:
                self.bot.active_creature = action.thing
        else:
            # Handle attack
            skill = action.thing
            attacker = self.player.active_creature if action.player == self.player else self.bot.active_creature
            defender = self.bot.active_creature if action.player == self.player else self.player.active_creature
            
            damage = self.calculate_damage(skill, attacker, defender)
            defender.hp = max(0, defender.hp - damage)
            
            # Force swap if creature fainted
            if defender.hp == 0:
                self.handle_fainted_creature(defender)

    def calculate_damage(self, skill: Skill, attacker: Creature, defender: Creature) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, attack_type: str, defend_type: str) -> float:
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def handle_fainted_creature(self, fainted_creature: Creature):
        player = self.player if fainted_creature in self.player.creatures else self.bot
        available_creatures = self.get_available_creatures(player)
        
        if available_creatures:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            new_creature = self._wait_for_choice(player, creature_choices).thing
            player.active_creature = new_creature

    def check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
