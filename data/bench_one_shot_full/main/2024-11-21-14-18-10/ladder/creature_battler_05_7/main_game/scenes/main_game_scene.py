from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        
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
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if player_action is None:  # No valid actions available
                break
                
            bot_action = self.get_player_action(self.bot)
            if bot_action is None:  # No valid actions available
                break
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_available_creatures(self, player: Player) -> list[Creature]:
        return [
            creature 
            for creature in player.creatures 
            if creature.hp > 0 and creature != player.active_creature
        ]

    def get_player_action(self, current_player: Player):
        # If current creature is knocked out and no swaps available, return None
        if current_player.active_creature.hp <= 0:
            available = [c for c in current_player.creatures if c.hp > 0]
            if not available:
                return None
            # Force swap if current creature is knocked out
            creature_choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(current_player, creature_choices)
            current_player.active_creature = choice.thing
            self._show_text(self.player, f"{'You' if current_player == self.player else 'Foe'} sent out {choice.thing.display_name}!")
            return choice

        while True:  # Allow returning to main menu with Back button
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(current_player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Show skills
                skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
                if current_player == self.player:  # Only add back button for human player
                    back_button = Button("Back")
                    action = self._wait_for_choice(current_player, skill_choices + [back_button])
                    if action == back_button:
                        continue
                    return action
                return self._wait_for_choice(current_player, skill_choices)
            else:
                # Show available creatures
                available_creatures = self.get_available_creatures(current_player)
                if not available_creatures:  # If no creatures to swap to, force attack
                    skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
                    return self._wait_for_choice(current_player, skill_choices)
                    
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                if current_player == self.player:  # Only add back button for human player
                    back_button = Button("Back")
                    action = self._wait_for_choice(current_player, creature_choices + [back_button])
                    if action == back_button:
                        continue
                    return action
                return self._wait_for_choice(current_player, creature_choices)

    def resolve_turn(self, player_action, bot_action):
        if player_action is None or bot_action is None:
            return
            
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
            self._show_text(self.player, f"You swapped to {player_action.thing.display_name}!")
            
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            self._show_text(self.player, f"Foe swapped to {bot_action.thing.display_name}!")

        # Then handle attacks
        first, second = self.determine_turn_order(player_action, bot_action)
        self.execute_action(first)
        if self.check_battle_end():
            return
        self.execute_action(second)

    def determine_turn_order(self, player_action, bot_action):
        if isinstance(player_action.thing, Creature) or isinstance(bot_action.thing, Creature):
            return (player_action, bot_action) if isinstance(bot_action.thing, Creature) else (bot_action, player_action)
            
        player_speed = self.player.active_creature.speed
        bot_speed = self.bot.active_creature.speed
        
        if player_speed > bot_speed:
            return (player_action, bot_action)
        elif bot_speed > player_speed:
            return (bot_action, player_action)
        else:
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def execute_action(self, action):
        if isinstance(action.thing, Creature):
            return
            
        attacker = self.player if action.thing in self.player.active_creature.skills else self.bot
        defender = self.bot if attacker == self.player else self.player
        
        skill = action.thing
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name}! Dealt {damage} damage!")
        
        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} was knocked out!")
            self.handle_knockout(defender)

    def calculate_damage(self, attacker: Creature, defender: Creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if not available_creatures:
            return
            
        creature_choices = [SelectThing(c) for c in available_creatures]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        self._show_text(self.player, f"{'You' if player == self.player else 'Foe'} sent out {choice.thing.display_name}!")

    def check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        if not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene") 
            return True
            
        return False
