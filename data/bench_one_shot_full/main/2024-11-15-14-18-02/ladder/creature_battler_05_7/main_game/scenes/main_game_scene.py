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
Opponent's {o_creature.display_name}: {o_creature.hp}/{o_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
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
                # Reset creatures before ending
                self.reset_creatures()
                self._quit_whole_game()
                return

    def reset_creatures(self):
        # Reset player creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
            
        # Reset opponent creatures
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            back_button = Button("Back")
            skill_choice = self._wait_for_choice(player, skill_choices + [back_button])
            
            if skill_choice == back_button:
                return self.get_player_action(player)
            return ("attack", skill_choice.thing)
            
        else:
            # Show available creatures
            available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            back_button = Button("Back")
            creature_choice = self._wait_for_choice(player, creature_choices + [back_button])
            
            if creature_choice == back_button:
                return self.get_player_action(player)
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
            if self.opponent.active_creature.hp > 0 and self.player.active_creature.hp > 0:
                self.execute_attack(second[0], second[1])

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
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show result
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"It dealt {final_damage} damage!")

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        # Check if either player has any creatures left
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        opponent_has_creatures = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not opponent_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        # Force swap if active creature is knocked out
        if self.player.active_creature.hp <= 0:
            available = [c for c in self.player.creatures if c.hp > 0]
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(self.player, choices)
            self.player.active_creature = choice.thing
            
        if self.opponent.active_creature.hp <= 0:
            available = [c for c in self.opponent.creatures if c.hp > 0]
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(self.opponent, choices)
            self.opponent.active_creature = choice.thing
            
        return False
