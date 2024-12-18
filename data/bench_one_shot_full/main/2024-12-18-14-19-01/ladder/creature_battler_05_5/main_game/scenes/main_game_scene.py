from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
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

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.bot.display_name}'s {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

What will {player_creature.display_name} do?
> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                continue

            # Resolve actions
            self.resolve_turn(player_action, bot_action)

            # Check for battle end
            if self.check_battle_end():
                # Transition back to main menu after battle ends
                self._transition_to_scene("MainMenuScene")
                return

    def get_player_action(self, player):
        while True:
            choice = self._wait_for_choice(player, [
                Button("Attack"),
                Button("Swap"),
            ])

            if choice.display_name == "Attack":
                skills = [SelectThing(skill) for skill in player.active_creature.skills]
                skills.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skills)
                
                if not isinstance(skill_choice, Button):
                    return ("attack", skill_choice.thing)

            elif choice.display_name == "Swap":
                available_creatures = [
                    SelectThing(c) for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                
                if not available_creatures:
                    self._show_text(player, "No creatures available to swap!")
                    continue
                    
                available_creatures.append(Button("Back"))
                swap_choice = self._wait_for_choice(player, available_creatures)
                
                if not isinstance(swap_choice, Button):
                    return ("swap", swap_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"Go {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.bot, f"Go {bot_action[1].display_name}!")

        # Then handle attacks
        first = self.player
        first_action = player_action
        second = self.bot
        second_action = bot_action

        if bot_action[0] == "attack" and player_action[0] == "attack":
            if self.bot.active_creature.speed > self.player.active_creature.speed:
                first = self.bot
                first_action = bot_action
                second = self.player
                second_action = player_action
            elif self.bot.active_creature.speed == self.player.active_creature.speed:
                if random.random() < 0.5:
                    first = self.bot
                    first_action = bot_action
                    second = self.player
                    second_action = player_action

        if first_action[0] == "attack":
            self.execute_attack(first, first_action[1], second)
            
        if second.active_creature.hp > 0 and second_action[0] == "attack":
            self.execute_attack(second, second_action[1], first)

    def execute_attack(self, attacker, skill, defender):
        target = defender.active_creature
        
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - target.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / target.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, target.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        target.hp = max(0, target.hp - final_damage)
        
        effectiveness = ""
        if multiplier > 1:
            effectiveness = "It's super effective!"
        elif multiplier < 1:
            effectiveness = "It's not very effective..."
            
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}! {effectiveness}")
        
        if target.hp <= 0:
            self._show_text(defender, f"{target.display_name} was knocked out!")
            self.handle_knockout(defender)

    def get_type_multiplier(self, skill_type, target_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(target_type, 1.0)

    def handle_knockout(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if not available_creatures:
            return
            
        self._show_text(player, "Choose next creature!")
        swap_choices = [SelectThing(c) for c in available_creatures]
        choice = self._wait_for_choice(player, swap_choices)
        player.active_creature = choice.thing
        self._show_text(player, f"Go {choice.thing.display_name}!")

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_alive:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
