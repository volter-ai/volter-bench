from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Reset creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Opponent's {self.opponent.active_creature.display_name}: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp} HP

What will you do?
> Attack
> Swap
"""

    def run(self):
        while True:
            # Get player actions
            player_action = self.get_player_action(self.player)
            opponent_action = self.get_player_action(self.opponent)
            
            # Resolve actions
            self.resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()  # <-- Added this line to properly exit

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
                    SelectThing(creature) 
                    for creature in player.creatures 
                    if creature != player.active_creature and creature.hp > 0
                ]
                
                if available_creatures:
                    back_button = Button("Back")
                    creature_choice = self._wait_for_choice(player, available_creatures + [back_button])
                    
                    if creature_choice != back_button:
                        return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if opponent_action[0] == "swap":
            self.opponent.active_creature = opponent_action[1]
            
        # Then handle attacks
        if player_action[0] == "attack" and opponent_action[0] == "attack":
            # Determine order
            if self.player.active_creature.speed > self.opponent.active_creature.speed:
                first, second = (self.player, player_action[1]), (self.opponent, opponent_action[1])
            elif self.player.active_creature.speed < self.opponent.active_creature.speed:
                first, second = (self.opponent, opponent_action[1]), (self.player, player_action[1])
            else:
                if random.random() < 0.5:
                    first, second = (self.player, player_action[1]), (self.opponent, opponent_action[1])
                else:
                    first, second = (self.opponent, opponent_action[1]), (self.player, player_action[1])
                    
            # Execute attacks
            self.execute_attack(first[0], first[1])
            if second[0].active_creature.hp > 0:  # Only do second attack if target still alive
                self.execute_attack(second[0], second[1])

    def execute_attack(self, attacker, skill):
        defender = self.opponent if attacker == self.player else self.player
        
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show result
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {final_damage} damage!")
        
        # Handle fainting
        if defender.active_creature.hp <= 0:
            self._show_text(defender, f"{defender.active_creature.display_name} fainted!")
            self.handle_fainted_creature(defender)

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def handle_fainted_creature(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            choices = [SelectThing(c) for c in available_creatures]
            self._show_text(player, "Choose next creature:")
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        opponent_has_creatures = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not opponent_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
