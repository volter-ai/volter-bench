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
> Swap
"""

    def calculate_damage(self, attacker: Creature, defender: Creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = 1.0  # Normal type is neutral against everything
        
        if skill.skill_type != "normal":
            # Type matchup matrix
            type_matchups = {
                "fire": {
                    "leaf": 2.0,   # Super effective
                    "water": 0.5   # Not very effective
                },
                "water": {
                    "fire": 2.0,   # Super effective
                    "leaf": 0.5    # Not very effective
                },
                "leaf": {
                    "water": 2.0,  # Super effective
                    "fire": 0.5    # Not very effective
                }
            }
            
            # Get effectiveness if there's a matchup
            if skill.skill_type in type_matchups:
                if defender.creature_type in type_matchups[skill.skill_type]:
                    effectiveness = type_matchups[skill.skill_type][defender.creature_type]

        return int(raw_damage * effectiveness)

    def get_available_creatures(self, player: Player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_turn(self, attacker: Player, defender: Player):
        # Get action choice
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choice = self._wait_for_choice(attacker, [attack_button, swap_button])

        if choice == attack_button:
            # Choose skill
            skill_choices = [SelectThing(s) for s in attacker.active_creature.skills]
            back_button = Button("Back")
            skill_choice = self._wait_for_choice(attacker, skill_choices + [back_button])
            
            if skill_choice == back_button:
                return self.handle_turn(attacker, defender)
            
            return ("attack", skill_choice.thing)
        else:
            # Choose creature to swap to
            available = self.get_available_creatures(attacker)
            if not available:
                self._show_text(attacker, "No creatures available to swap to!")
                return self.handle_turn(attacker, defender)
                
            swap_choices = [SelectThing(c) for c in available]
            back_button = Button("Back")
            swap_choice = self._wait_for_choice(attacker, swap_choices + [back_button])
            
            if swap_choice == back_button:
                return self.handle_turn(attacker, defender)
                
            return ("swap", swap_choice.thing)

    def run(self):
        while True:
            # Get actions
            player_action = self.handle_turn(self.player, self.bot)
            bot_action = self.handle_turn(self.bot, self.player)

            # Handle swaps first
            for actor, action in [(self.player, player_action), (self.bot, bot_action)]:
                if action[0] == "swap":
                    actor.active_creature = action[1]
                    self._show_text(self.player, f"{actor.display_name} swapped to {action[1].display_name}!")

            # Determine action order based on speed
            player_speed = self.player.active_creature.speed
            bot_speed = self.bot.active_creature.speed
            
            if player_speed == bot_speed:
                # If speeds are equal, randomly choose order
                actors = [(self.player, player_action), (self.bot, bot_action)]
                random.shuffle(actors)  # Randomly reorder the list
            else:
                # Sort by speed (higher speed goes first)
                actors = [(self.player, player_action), (self.bot, bot_action)]
                actors.sort(key=lambda x: x[0].active_creature.speed, reverse=True)

            # Handle attacks in determined order
            for actor, action in actors:
                if action[0] == "attack":
                    defender = self.bot if actor == self.player else self.player
                    damage = self.calculate_damage(actor.active_creature, defender.active_creature, action[1])
                    defender.active_creature.hp -= damage
                    self._show_text(self.player, 
                        f"{actor.display_name}'s {actor.active_creature.display_name} used {action[1].display_name}! "
                        f"Dealt {damage} damage!")

                    # Check for fainted creature
                    if defender.active_creature.hp <= 0:
                        defender.active_creature.hp = 0
                        self._show_text(self.player, 
                            f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
                        
                        # Check for available creatures
                        available = self.get_available_creatures(defender)
                        if not available:
                            self._show_text(self.player, 
                                f"{'You won!' if defender == self.bot else 'You lost!'}")
                            self._transition_to_scene("MainMenuScene")
                            return
                            
                        # Force swap
                        swap_choices = [SelectThing(c) for c in available]
                        swap_choice = self._wait_for_choice(defender, swap_choices)
                        defender.active_creature = swap_choice.thing
                        self._show_text(self.player,
                            f"{defender.display_name} sent out {swap_choice.thing.display_name}!")
