from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Initialize creatures
        for p in [self.player, self.opponent]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

    def __str__(self):
        p_creature = self.player.active_creature
        o_creature = self.opponent.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {o_creature.display_name}: {o_creature.hp}/{o_creature.max_hp} HP

> Attack - Use a skill
> Swap - Switch active creature
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            opponent_action = self.get_player_action(self.opponent)
            
            # Resolve actions
            self.resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Transition back to main menu instead of just breaking
                self._transition_to_scene("MainMenuScene")
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
                
                if skill_choice != back_button:
                    return ("attack", skill_choice.thing)
                    
            else:
                available_creatures = [
                    c for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                if available_creatures:
                    creatures = [SelectThing(c) for c in available_creatures]
                    back_button = Button("Back")
                    creature_choice = self._wait_for_choice(player, creatures + [back_button])
                    
                    if creature_choice != back_button:
                        return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, opponent_action):
        actions = [(self.player, player_action), (self.opponent, opponent_action)]
        
        # Resolve swaps first
        for player, action in actions:
            if action[0] == "swap":
                self._show_text(player, f"{player.display_name} swaps to {action[1].display_name}!")
                player.active_creature = action[1]
        
        # Then resolve attacks based on speed
        attack_actions = [(p, a) for p, a in actions if a[0] == "attack"]
        if len(attack_actions) == 2:
            # Sort by speed
            attack_actions.sort(
                key=lambda x: x[0].active_creature.speed, 
                reverse=True
            )
            
        for attacker, action in attack_actions:
            if attacker == self.player:
                defender = self.opponent
            else:
                defender = self.player
                
            self.execute_attack(attacker, defender, action[1])
            
            # Force swap if creature fainted
            if defender.active_creature.hp <= 0:
                available_creatures = [c for c in defender.creatures if c.hp > 0]
                if available_creatures:
                    creatures = [SelectThing(c) for c in available_creatures]
                    choice = self._wait_for_choice(defender, creatures)
                    defender.active_creature = choice.thing
                    self._show_text(defender, f"{defender.display_name} sends out {choice.thing.display_name}!")

    def execute_attack(self, attacker, defender, skill):
        self._show_text(attacker, f"{attacker.active_creature.display_name} uses {skill.display_name}!")
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = (
                attacker.active_creature.attack + 
                skill.base_damage - 
                defender.active_creature.defense
            )
        else:
            raw_damage = (
                skill.base_damage * 
                attacker.active_creature.sp_attack / 
                defender.active_creature.sp_defense
            )
            
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(
            skill.skill_type, 
            defender.active_creature.creature_type
        )
        
        final_damage = int(raw_damage * effectiveness)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"It deals {final_damage} damage!")
        if effectiveness > 1:
            self._show_text(attacker, "It's super effective!")
        elif effectiveness < 1:
            self._show_text(attacker, "It's not very effective...")

    def get_type_effectiveness(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def check_battle_end(self):
        for player in [self.player, self.opponent]:
            if all(c.hp <= 0 for c in player.creatures):
                winner = self.opponent if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins the battle!")
                return True
        return False
