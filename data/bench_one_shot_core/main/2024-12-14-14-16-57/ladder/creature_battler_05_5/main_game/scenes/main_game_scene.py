from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        p_creature = self.player.active_creature
        o_creature = self.opponent.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Opponent's {o_creature.display_name}: {o_creature.hp}/{o_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                return
                
            # Opponent turn
            opponent_action = self.get_player_action(self.opponent)
            if not opponent_action:
                return
                
            # Resolve actions
            self.resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            if self.check_battle_end():
                return

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                skills = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skills + [back_button])
                
                if skill_choice == back_button:
                    continue
                    
                return {"type": "attack", "skill": skill_choice.thing}
                
            elif choice == swap_button:
                available_creatures = [
                    c for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                creatures = [SelectThing(creature) for creature in available_creatures]
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, creatures + [back_button])
                
                if creature_choice == back_button:
                    continue
                    
                return {"type": "swap", "creature": creature_choice.thing}

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"You switched to {player_action['creature'].display_name}!")
            
        if opponent_action["type"] == "swap":
            self.opponent.active_creature = opponent_action["creature"]
            self._show_text(self.player, f"Opponent switched to {opponent_action['creature'].display_name}!")

        # Then handle attacks
        actions = []
        if player_action["type"] == "attack":
            actions.append((self.player, player_action["skill"], self.opponent))
        if opponent_action["type"] == "attack":
            actions.append((self.opponent, opponent_action["skill"], self.player))

        # Sort by speed
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        if len(actions) == 2 and actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
            random.shuffle(actions)

        # Execute attacks
        for attacker, skill, defender in actions:
            self.execute_skill(attacker, skill, defender)
            if self.check_battle_end():
                return

    def execute_skill(self, attacker, skill, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Calculate type multiplier
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        
        # Calculate final damage
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)

        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name} on {defender.active_creature.display_name} for {final_damage} damage!")

        if defender.active_creature.hp == 0:
            self.handle_knockout(defender)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, player):
        self._show_text(self.player, f"{player.active_creature.display_name} was knocked out!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        if player == self.player:
            choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
        else:
            player.active_creature = available_creatures[0]
            self._show_text(self.player, f"Opponent sent out {player.active_creature.display_name}!")

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        opponent_alive = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_alive or not opponent_alive:
            winner = "You" if player_alive else "Opponent"
            self._show_text(self.player, f"{winner} won the battle!")
            
            # Reset creatures
            for creature in self.player.creatures + self.opponent.creatures:
                creature.hp = creature.max_hp
                
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
