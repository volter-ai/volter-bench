from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creatures to starting state
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

> Attack - Use a skill
> Swap - Switch active creature (if available)
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player):
        # Get available creatures for swapping
        available_creatures = [
            creature for creature in player.creatures 
            if creature.hp > 0 and creature != player.active_creature
        ]

        # Only show swap option if there are creatures to swap to
        choices = [Button("Attack")]
        if available_creatures:
            choices.append(Button("Swap"))
        
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            return self._wait_for_choice(player, skill_choices)
        else:
            # Show available creatures
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            return self._wait_for_choice(player, creature_choices)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
            self._show_text(self.player, f"You switched to {player_action.thing.display_name}!")
            
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            self._show_text(self.player, f"Foe switched to {bot_action.thing.display_name}!")

        # Then handle attacks
        first = self.player
        second = self.bot
        first_action = player_action
        second_action = bot_action
        
        if self.bot.active_creature.speed > self.player.active_creature.speed:
            first = self.bot
            second = self.player
            first_action = bot_action
            second_action = player_action
        elif self.bot.active_creature.speed == self.player.active_creature.speed:
            if random.random() < 0.5:
                first = self.bot
                second = self.player
                first_action = bot_action
                second_action = player_action

        # Execute attacks
        if isinstance(first_action.thing, Skill):
            self.execute_skill(first, second, first_action.thing)
        if isinstance(second_action.thing, Skill) and second.active_creature.hp > 0:
            self.execute_skill(second, first, second_action.thing)

        # Force swaps if needed
        self.handle_forced_swaps()

    def execute_skill(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        effectiveness = "It's super effective!" if multiplier > 1 else "It's not very effective..." if multiplier < 1 else ""
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! {effectiveness}")

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def handle_forced_swaps(self):
        for player in [self.player, self.bot]:
            if player.active_creature.hp <= 0:
                available_creatures = [c for c in player.creatures if c.hp > 0]
                if available_creatures:
                    if len(available_creatures) == 1:
                        player.active_creature = available_creatures[0]
                        self._show_text(self.player, 
                            f"{'You' if player == self.player else 'Foe'} switched to {available_creatures[0].display_name}!")
                    else:
                        creature_choices = [SelectThing(c) for c in available_creatures]
                        choice = self._wait_for_choice(player, creature_choices)
                        player.active_creature = choice.thing
                        self._show_text(self.player,
                            f"{'You' if player == self.player else 'Foe'} switched to {choice.thing.display_name}!")

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures or not bot_has_creatures:
            winner = "You win!" if player_has_creatures else "You lose!"
            self._show_text(self.player, f"Battle Over! {winner}")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
