from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        # Initialize creatures
        for p in [self.player, self.bot]:
            p.active_creature = p.creatures[0]
            for c in p.creatures:
                c.hp = c.max_hp

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

> Attack
> Swap (if available)
"""

    def calculate_damage(self, attacker: Creature, defender: Creature, skill):
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

    def get_available_creatures(self, player: Player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_turn(self, attacker: Player, defender: Player):
        while True:  # Allow returning to main menu with Back button
            # Get action choice
            choices = [Button("Attack")]
            
            # Only add swap option if there are creatures available to swap to
            available_creatures = self.get_available_creatures(attacker)
            if available_creatures:
                choices.append(Button("Swap"))
                
            choice = self._wait_for_choice(attacker, choices)
            
            if choice.display_name == "Attack":
                # Choose skill with Back option
                skill_choices = [SelectThing(s) for s in attacker.active_creature.skills]
                skill_choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(attacker, skill_choices)
                
                if skill_choice.display_name == "Back":
                    continue  # Return to main menu
                    
                return ("attack", skill_choice.thing)
            else:  # Swap
                # Choose creature with Back option
                creature_choices = [SelectThing(c) for c in available_creatures]
                creature_choices.append(Button("Back"))
                creature_choice = self._wait_for_choice(attacker, creature_choices)
                
                if creature_choice.display_name == "Back":
                    continue  # Return to main menu
                    
                return ("swap", creature_choice.thing)

    def run(self):
        while True:
            # Get actions
            p_action = self.handle_turn(self.player, self.bot)
            b_action = self.handle_turn(self.bot, self.player)
            
            # Handle swaps first
            if p_action[0] == "swap":
                self.player.active_creature = p_action[1]
                self._show_text(self.player, f"You sent out {p_action[1].display_name}!")
            if b_action[0] == "swap":
                self.bot.active_creature = b_action[1]
                self._show_text(self.player, f"Foe sent out {b_action[1].display_name}!")
                
            # Handle attacks based on speed (with random tiebreaker)
            actions = []
            if p_action[0] == "attack":
                actions.append((self.player, self.bot, p_action[1]))
            if b_action[0] == "attack":
                actions.append((self.bot, self.player, b_action[1]))
                
            # Sort by speed, using random tiebreaker for equal speeds
            actions.sort(key=lambda x: (x[0].active_creature.speed, random.random()), reverse=True)
            
            for attacker, defender, skill in actions:
                damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
                defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
                self._show_text(self.player, 
                    f"{attacker.active_creature.display_name} used {skill.display_name}! "
                    f"Dealt {damage} damage to {defender.active_creature.display_name}!")
                
                if defender.active_creature.hp == 0:
                    available = self.get_available_creatures(defender)
                    if not available:
                        self._show_text(self.player, 
                            "You win!" if defender == self.bot else "You lose!")
                        self._quit_whole_game()
                    else:
                        creature_choices = [SelectThing(c) for c in available]
                        new_creature = self._wait_for_choice(defender, creature_choices).thing
                        defender.active_creature = new_creature
                        self._show_text(self.player,
                            f"{'You' if defender == self.player else 'Foe'} sent out {new_creature.display_name}!")
