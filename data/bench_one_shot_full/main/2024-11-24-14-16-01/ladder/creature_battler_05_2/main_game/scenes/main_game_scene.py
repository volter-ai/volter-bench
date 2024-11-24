from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
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
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
VS
{self.bot.display_name}'s {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap
"""

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
                # Return to main menu after battle ends
                self._transition_to_scene("MainMenuScene")
                return

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            skill_choices.append(back_button)
            choice = self._wait_for_choice(player, skill_choices)
            if choice == back_button:
                return None
            return ("attack", choice.thing)
            
        elif choice == swap_button:
            # Show available creatures
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            if not available_creatures:
                self._show_text(player, "No other creatures available!")
                return None
                
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            creature_choices.append(back_button)
            choice = self._wait_for_choice(player, creature_choices)
            if choice == back_button:
                return None
            return ("swap", choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Determine order
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Swaps go first
        swap_actions = [a for a in actions if a[1][0] == "swap"]
        attack_actions = [a for a in actions if a[1][0] == "attack"]
        
        # Execute swaps
        for player, (_, creature) in swap_actions:
            player.active_creature = creature
            self._show_text(player, f"{player.display_name} swapped to {creature.display_name}!")
            
        # Execute attacks in speed order
        if len(attack_actions) == 2:
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                attack_actions = attack_actions
            elif self.player.active_creature.speed < self.bot.active_creature.speed:
                attack_actions = list(reversed(attack_actions))
            else:
                if random.random() < 0.5:
                    attack_actions = list(reversed(attack_actions))
                    
        for attacker, (_, skill) in attack_actions:
            if attacker == self.player:
                defender = self.bot
            else:
                defender = self.player
                
            self.execute_attack(attacker, defender, skill)
            
            # Force swap if creature fainted
            if defender.active_creature.hp <= 0:
                available_creatures = [c for c in defender.creatures if c.hp > 0]
                if available_creatures:
                    creature_choices = [SelectThing(creature) for creature in available_creatures]
                    choice = self._wait_for_choice(defender, creature_choices)
                    defender.active_creature = choice.thing
                    self._show_text(defender, f"{defender.display_name} sent out {choice.thing.display_name}!")

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show message
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        if effectiveness == 2:
            self._show_text(attacker, "It's super effective!")
        elif effectiveness == 0.5:
            self._show_text(attacker, "It's not very effective...")

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1
        
        effectiveness_chart = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1)

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
