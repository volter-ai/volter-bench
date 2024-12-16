from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self._reset_creatures()

    def _reset_creatures(self):
        # Reset all creatures to max HP
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

> Attack
> Swap
"""

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill):
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

    def _get_available_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def _has_valid_creatures(self, player):
        return any(c.hp > 0 for c in player.creatures)

    def _handle_turn_choice(self, player):
        # First handle knocked out active creature
        if player.active_creature.hp <= 0:
            available = self._get_available_creatures(player)
            if not available:
                return False  # No creatures left
            swap_choices = [SelectThing(c) for c in available]
            swap = self._wait_for_choice(player, swap_choices)
            player.active_creature = swap.thing
            self._show_text(self.player, f"{player.display_name} sent out {swap.thing.display_name}!")

        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")

        while True:
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(back_button)
                skill_choice = self._wait_for_choice(player, skill_choices)
                
                if skill_choice == back_button:
                    continue
                    
                return ("attack", skill_choice.thing)
                
            elif choice == swap_button:
                available_creatures = self._get_available_creatures(player)
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choices.append(back_button)
                creature_choice = self._wait_for_choice(player, creature_choices)
                
                if creature_choice == back_button:
                    continue
                    
                return ("swap", creature_choice.thing)

    def run(self):
        while True:
            # Player turn
            if not self._has_valid_creatures(self.player):
                self._show_text(self.player, "Bot won the battle!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return
            
            player_action = self._handle_turn_choice(self.player)
            if player_action is False:  # No valid moves possible
                self._show_text(self.player, "Bot won the battle!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return

            # Bot turn
            if not self._has_valid_creatures(self.bot):
                self._show_text(self.player, "You won the battle!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return
            
            bot_action = self._handle_turn_choice(self.bot)
            if bot_action is False:  # No valid moves possible
                self._show_text(self.player, "You won the battle!")
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return
            
            # Resolution phase
            actions = [(self.player, player_action), (self.bot, bot_action)]
            
            # Handle swaps first
            for player, (action_type, target) in actions:
                if action_type == "swap":
                    player.active_creature = target
                    self._show_text(self.player, f"{player.display_name} swapped to {target.display_name}!")
            
            # Handle attacks
            attack_actions = [(p, a) for p, a in actions if a[0] == "attack"]
            attack_actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
            
            for attacker, (_, skill) in attack_actions:
                defender = self.bot if attacker == self.player else self.player
                damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
                defender.active_creature.hp -= damage
                self._show_text(self.player, 
                    f"{attacker.active_creature.display_name} used {skill.display_name} for {damage} damage!")
                
                if defender.active_creature.hp <= 0:
                    defender.active_creature.hp = 0
                    self._show_text(self.player, 
                        f"{defender.active_creature.display_name} was knocked out!")
