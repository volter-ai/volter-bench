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

> Attack
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            opponent_action = self.get_player_action(self.opponent)
            
            self.resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()  # <-- Fixed: Properly end the game when battle is over

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
                    
            else:  # Swap
                available_creatures = [
                    SelectThing(creature) 
                    for creature in player.creatures 
                    if creature != player.active_creature and creature.hp > 0
                ]
                
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, available_creatures + [back_button])
                
                if creature_choice != back_button:
                    return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, opponent_action):
        actions = [(self.player, player_action), (self.opponent, opponent_action)]
        
        # Resolve swaps first
        for player, action in actions:
            if action[0] == "swap":
                player.active_creature = action[1]
                self._show_text(player, f"Swapped to {action[1].display_name}!")
        
        # Then resolve attacks based on speed
        if player_action[0] == "attack" and opponent_action[0] == "attack":
            if self.player.active_creature.speed > self.opponent.active_creature.speed:
                first, second = actions
            elif self.player.active_creature.speed < self.opponent.active_creature.speed:
                second, first = actions
            else:
                if random.random() < 0.5:
                    first, second = actions
                else:
                    second, first = actions
                    
            for attacker, action in [first, second]:
                if action[0] == "attack":
                    self.execute_attack(attacker, action[1])

    def execute_attack(self, attacker, skill):
        if attacker == self.player:
            defender = self.opponent
        else:
            defender = self.player
            
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
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        
        if effectiveness == 2:
            self._show_text(attacker, "It's super effective!")
        elif effectiveness == 0.5:
            self._show_text(attacker, "It's not very effective...")
            
        # Force swap if creature fainted
        if defender.active_creature.hp == 0:
            available_creatures = [c for c in defender.creatures if c.hp > 0]
            if available_creatures:
                if defender == self.player:
                    choices = [SelectThing(c) for c in available_creatures]
                    choice = self._wait_for_choice(defender, choices)
                    defender.active_creature = choice.thing
                else:
                    defender.active_creature = available_creatures[0]

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1
        
        effectiveness_chart = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1)

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        opponent_has_creatures = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost!")
            return True
        elif not opponent_has_creatures:
            self._show_text(self.player, "You won!")
            return True
            
        return False
