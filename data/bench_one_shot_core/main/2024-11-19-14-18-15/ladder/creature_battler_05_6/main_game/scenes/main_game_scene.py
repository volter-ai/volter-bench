from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]
        
        # Reset creature HP
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Opponent's {self.opponent.active_creature.display_name}: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp} HP

Your other creatures:
{self._format_bench(self.player)}

Opponent's other creatures:
{self._format_bench(self.opponent)}
"""

    def _format_bench(self, player):
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" 
                         for c in player.creatures if c != player.active_creature])

    def run(self):
        while True:
            # Player turn
            player_action = self._handle_turn(self.player)
            if not player_action:
                return
                
            # Opponent turn
            opponent_action = self._handle_turn(self.opponent)
            if not opponent_action:
                return
                
            # Resolve actions
            self._resolve_actions(player_action, opponent_action)
            
            # Check for battle end
            if self._check_battle_end():
                return

    def _handle_turn(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            back_button = Button("Back")
            skill_choice = self._wait_for_choice(player, skill_choices + [back_button])
            
            if skill_choice == back_button:
                return self._handle_turn(player)
            return ("attack", skill_choice.thing)
            
        else:
            # Show available creatures
            available_creatures = [c for c in player.creatures 
                                if c != player.active_creature and c.hp > 0]
            if not available_creatures:
                self._show_text(player, "No other creatures available!")
                return self._handle_turn(player)
                
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            back_button = Button("Back")
            creature_choice = self._wait_for_choice(player, creature_choices + [back_button])
            
            if creature_choice == back_button:
                return self._handle_turn(player)
            return ("swap", creature_choice.thing)

    def _resolve_actions(self, player_action, opponent_action):
        actions = [player_action, opponent_action]
        actors = [self.player, self.opponent]
        
        # Handle swaps first
        for i, (action, actor) in enumerate(zip(actions, actors)):
            if action[0] == "swap":
                old_creature = actor.active_creature
                actor.active_creature = action[1]
                self._show_text(actor, f"{old_creature.display_name} swaps out for {action[1].display_name}!")

        # Determine attack order
        if all(action[0] == "attack" for action in actions):
            if self.player.active_creature.speed > self.opponent.active_creature.speed:
                order = [0, 1]
            elif self.player.active_creature.speed < self.opponent.active_creature.speed:
                order = [1, 0]
            else:
                order = [0, 1] if random.random() < 0.5 else [1, 0]
        else:
            order = [0, 1]

        # Execute attacks
        for i in order:
            if actions[i][0] == "attack":
                self._execute_attack(actors[i], actors[1-i], actions[i][1])

    def _execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         defender.active_creature.defense)
        else:
            raw_damage = (skill.base_damage * 
                         attacker.active_creature.sp_attack / 
                         defender.active_creature.sp_defense)
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, 
                                             defender.active_creature.creature_type)
        
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, 
                       f"{attacker.active_creature.display_name} uses {skill.display_name}!")
        self._show_text(defender, 
                       f"{defender.active_creature.display_name} takes {final_damage} damage!")
        
        if defender.active_creature.hp == 0:
            self._handle_knockout(defender)

    def _get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def _handle_knockout(self, player):
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        self._show_text(player, f"Go, {choice.thing.display_name}!")

    def _check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        opponent_alive = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_alive or not opponent_alive:
            winner = self.player if player_alive else self.opponent
            self._show_text(self.player, 
                          "You win!" if winner == self.player else "You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
