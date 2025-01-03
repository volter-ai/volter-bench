from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
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

    def reset_creatures_state(self):
        # Reset all creatures back to full HP
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = None

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
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Reset creature state before leaving scene
                self.reset_creatures_state()
                break

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(s) for s in player.active_creature.skills]
            skill_choices.append(back_button)
            choice = self._wait_for_choice(player, skill_choices)
            if choice == back_button:
                return None
            return ("attack", choice.thing)
            
        elif choice == swap_button:
            # Show available creatures
            available = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            if not available:
                self._show_text(player, "No other creatures available!")
                return None
                
            creature_choices = [SelectThing(c) for c in available]
            creature_choices.append(back_button)
            choice = self._wait_for_choice(player, creature_choices)
            if choice == back_button:
                return None
            return ("swap", choice.thing)

    def resolve_actions(self, player_action, bot_action):
        actions = [player_action, bot_action]
        actors = [self.player, self.bot]
        
        # Handle swaps first
        for i, (action, actor) in enumerate(zip(actions, actors)):
            if action[0] == "swap":
                actor.active_creature = action[1]
                self._show_text(actor, f"Swapped to {action[1].display_name}!")
                
        # Then handle attacks in speed order
        if all(a[0] == "attack" for a in actions):
            # Sort by speed
            pairs = list(zip(actions, actors))
            pairs.sort(key=lambda x: x[1].active_creature.speed, reverse=True)
            
            for (action, attacker), defender in zip(pairs, [actors[1], actors[0]]):
                self.execute_attack(attacker, defender, action[1])

    def execute_attack(self, attacker, defender, skill):
        a_creature = attacker.active_creature
        d_creature = defender.active_creature
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = a_creature.attack + skill.base_damage - d_creature.defense
        else:
            raw_damage = (a_creature.sp_attack / d_creature.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, d_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        # Apply damage
        d_creature.hp = max(0, d_creature.hp - final_damage)
        self._show_text(attacker, f"{a_creature.display_name} used {skill.display_name}!")
        
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
        for player in [self.player, self.bot]:
            if all(c.hp <= 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                return True
                
            if player.active_creature.hp <= 0:
                available = [c for c in player.creatures if c.hp > 0]
                if available:
                    choices = [SelectThing(c) for c in available]
                    choice = self._wait_for_choice(player, choices)
                    player.active_creature = choice.thing
                    self._show_text(player, f"Switched to {choice.thing.display_name}!")
        return False
