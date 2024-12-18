from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.turn_actions = []

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.bot.display_name}'s {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap"""

    def reset_creatures_state(self, player):
        """Reset all creatures' HP to their max HP"""
        for creature in player.creatures:
            creature.hp = creature.max_hp

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        try:
            while True:
                # Player turn
                if not self.handle_turn(self.player):
                    return
                    
                # Bot turn
                if not self.handle_turn(self.bot):
                    return
                    
                # Resolution phase
                self.resolve_turn()
                
                # Reset for next turn
                self.turn_actions = []
        finally:
            # Always reset creature states when leaving the scene
            self.reset_creatures_state(self.player)
            self.reset_creatures_state(self.bot)

    def handle_turn(self, current_player):
        if self.check_knocked_out(current_player.active_creature):
            if not self.handle_forced_swap(current_player):
                return False
                
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choice = self._wait_for_choice(current_player, [attack_button, swap_button])
        
        if choice == attack_button:
            skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
            back_button = Button("Back")
            skill_choice = self._wait_for_choice(current_player, skill_choices + [back_button])
            
            if skill_choice == back_button:
                return self.handle_turn(current_player)
            
            self.turn_actions.append(("attack", current_player, skill_choice.thing))
            
        elif choice == swap_button:
            available_creatures = [
                creature for creature in current_player.creatures 
                if creature != current_player.active_creature and creature.hp > 0
            ]
            if not available_creatures:
                self._show_text(current_player, "No other creatures available!")
                return self.handle_turn(current_player)
                
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            back_button = Button("Back")
            creature_choice = self._wait_for_choice(current_player, creature_choices + [back_button])
            
            if creature_choice == back_button:
                return self.handle_turn(current_player)
                
            self.turn_actions.append(("swap", current_player, creature_choice.thing))
            
        return True

    def resolve_turn(self):
        # Handle swaps first
        for action_type, player, thing in self.turn_actions:
            if action_type == "swap":
                player.active_creature = thing
                self._show_text(self.player, f"{player.display_name} swapped to {thing.display_name}!")

        # Then handle attacks
        attacks = [(p, t) for type_, p, t in self.turn_actions if type_ == "attack"]
        if len(attacks) == 2:
            # Determine order based on speed
            p1, s1 = attacks[0]
            p2, s2 = attacks[1]
            
            if p1.active_creature.speed > p2.active_creature.speed:
                self.execute_attack(p1, s1, p2)
                if p2.active_creature.hp > 0:
                    self.execute_attack(p2, s2, p1)
            elif p1.active_creature.speed < p2.active_creature.speed:
                self.execute_attack(p2, s2, p1)
                if p1.active_creature.hp > 0:
                    self.execute_attack(p1, s1, p2)
            else:
                if random.random() < 0.5:
                    self.execute_attack(p1, s1, p2)
                    if p2.active_creature.hp > 0:
                        self.execute_attack(p2, s2, p1)
                else:
                    self.execute_attack(p2, s2, p1)
                    if p1.active_creature.hp > 0:
                        self.execute_attack(p1, s1, p2)

    def execute_attack(self, attacker, skill, defender):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        factor = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * factor)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        effectiveness = "It's super effective!" if factor > 1 else "It's not very effective..." if factor < 1 else ""
        self._show_text(self.player, 
            f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}! {effectiveness}")

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def check_knocked_out(self, creature):
        return creature.hp <= 0

    def handle_forced_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if not available_creatures:
            winner = self.bot if player == self.player else self.player
            self._show_text(self.player, f"Game Over! {winner.display_name} wins!")
            self._transition_to_scene("MainMenuScene")
            return False
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        return True
