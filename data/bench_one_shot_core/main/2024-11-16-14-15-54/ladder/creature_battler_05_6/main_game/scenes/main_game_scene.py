from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
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
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack - Use a skill
> Swap - Switch active creature
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Show skills
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skill_choices + [back_button])
                
                if skill_choice != back_button:
                    return ("attack", skill_choice.thing)
                    
            else:
                # Show available creatures
                available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, creature_choices + [back_button])
                
                if creature_choice != back_button:
                    return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Swaps go first
        for player, action in actions:
            if action[0] == "swap":
                self._show_text(player, f"{player.display_name} swapped to {action[1].display_name}!")
                player.active_creature = action[1]
        
        # Then attacks based on speed
        attack_actions = [(p, a) for p, a in actions if a[0] == "attack"]
        if len(attack_actions) == 2:
            # Sort by speed
            attack_actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
            
        for player, action in attack_actions:
            if player.active_creature.hp > 0:  # Only attack if still conscious
                target = self.bot if player == self.player else self.player
                self.execute_attack(player, target, action[1])
                
                # Force swap if knocked out
                if target.active_creature.hp <= 0:
                    available_creatures = [c for c in target.creatures if c.hp > 0]
                    if available_creatures:
                        creature_choices = [SelectThing(creature) for creature in available_creatures]
                        choice = self._wait_for_choice(target, creature_choices)
                        target.active_creature = choice.thing
                        self._show_text(target, f"{target.display_name} sent out {choice.thing.display_name}!")

    def execute_attack(self, attacker, defender, skill):
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        self._show_text(defender, f"{defender.active_creature.display_name} took {final_damage} damage!")

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)

    def check_battle_end(self):
        player_has_conscious = any(c.hp > 0 for c in self.player.creatures)
        bot_has_conscious = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_conscious or not bot_has_conscious:
            winner = self.player if player_has_conscious else self.bot
            self._show_text(self.player, f"{winner.display_name} wins the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
