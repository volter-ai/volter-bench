from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
Foe's {o_creature.display_name}: {o_creature.hp}/{o_creature.max_hp} HP

> Attack
> Swap"""

    def reset_creatures(self):
        """Reset all creatures to their initial state"""
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            # Bot turn  
            bot_action = self.get_player_action(self.opponent)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Reset creatures before ending
                self.reset_creatures()
                # Properly end the game
                self._quit_whole_game()

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self.get_attack_choice(player)
        else:
            return self.get_swap_choice(player)

    def get_attack_choice(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self.get_player_action(player)
        return ("attack", choice.thing)

    def get_swap_choice(self, player):
        available_creatures = [c for c in player.creatures 
                             if c != player.active_creature and c.hp > 0]
        
        if not available_creatures:
            self._show_text(player, "No creatures available to swap!")
            return self.get_player_action(player)
            
        choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        if choice == back_button:
            return self.get_player_action(player)
        return ("swap", choice.thing)

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if opponent_action[0] == "swap":
            self.opponent.active_creature = opponent_action[1]
            
        # Then handle attacks based on speed
        if player_action[0] == "attack" and opponent_action[0] == "attack":
            if self.player.active_creature.speed > self.opponent.active_creature.speed:
                self.execute_attack(self.player, player_action[1], self.opponent)
                self.execute_attack(self.opponent, opponent_action[1], self.player)
            elif self.player.active_creature.speed < self.opponent.active_creature.speed:
                self.execute_attack(self.opponent, opponent_action[1], self.player)
                self.execute_attack(self.player, player_action[1], self.opponent)
            else:
                if random.random() < 0.5:
                    self.execute_attack(self.player, player_action[1], self.opponent)
                    self.execute_attack(self.opponent, opponent_action[1], self.player)
                else:
                    self.execute_attack(self.opponent, opponent_action[1], self.player)
                    self.execute_attack(self.player, player_action[1], self.opponent)

    def execute_attack(self, attacker, skill, defender):
        if attacker.active_creature.hp <= 0:
            return
            
        target = defender.active_creature
        
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         target.defense)
        else:
            raw_damage = (attacker.active_creature.sp_attack / 
                         target.sp_defense * 
                         skill.base_damage)
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, target.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        target.hp = max(0, target.hp - final_damage)
        
        self._show_text(attacker, 
                       f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender,
                       f"{target.display_name} took {final_damage} damage!")
        
        if target.hp <= 0:
            self.handle_knockout(defender)

    def get_type_multiplier(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def handle_knockout(self, player):
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        choices = [SelectThing(c) for c in available_creatures]
        self._show_text(player, "Choose next creature:")
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        opponent_alive = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_alive or not opponent_alive:
            if player_alive:
                self._show_text(self.player, "You won!")
            else:
                self._show_text(self.player, "You lost!")
            return True
        return False
