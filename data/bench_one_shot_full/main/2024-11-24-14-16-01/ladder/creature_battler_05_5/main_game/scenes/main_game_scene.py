from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        
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
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            opponent_action = self.get_player_action(self.opponent)
            
            self.resolve_actions(player_action, opponent_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()  # <-- Added this line to properly end the game

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
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, available_creatures + [back_button])
                
                if creature_choice != back_button:
                    return ("swap", creature_choice.thing)

    def resolve_actions(self, player_action, opponent_action):
        first_action, second_action = self.determine_action_order(player_action, opponent_action)
        
        self.execute_action(*first_action)
        self.execute_action(*second_action)
        
        # Force swaps if needed
        self.handle_fainted_creatures()

    def determine_action_order(self, player_action, opponent_action):
        # Swaps always go first
        if player_action[0] == "swap" and opponent_action[0] != "swap":
            return (player_action, opponent_action)
        elif opponent_action[0] == "swap" and player_action[0] != "swap":
            return (opponent_action, player_action)
            
        # Otherwise use speed
        if self.player.active_creature.speed > self.opponent.active_creature.speed:
            return (player_action, opponent_action)
        elif self.opponent.active_creature.speed > self.player.active_creature.speed:
            return (opponent_action, player_action)
        else:
            if random.random() < 0.5:
                return (player_action, opponent_action)
            return (opponent_action, player_action)

    def execute_action(self, action_type, action_data):
        if action_type == "swap":
            if action_data in self.player.creatures:
                self.player.active_creature = action_data
            else:
                self.opponent.active_creature = action_data
        else:  # attack
            skill = action_data
            attacker = self.player.active_creature if skill in self.player.active_creature.skills else self.opponent.active_creature
            defender = self.opponent.active_creature if attacker == self.player.active_creature else self.player.active_creature
            
            damage = self.calculate_damage(attacker, defender, skill)
            defender.hp = max(0, defender.hp - damage)

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_fainted_creatures(self):
        for player in [self.player, self.opponent]:
            if player.active_creature.hp <= 0:
                available_creatures = [c for c in player.creatures if c.hp > 0]
                if available_creatures:
                    choices = [SelectThing(c) for c in available_creatures]
                    choice = self._wait_for_choice(player, choices)
                    player.active_creature = choice.thing

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
