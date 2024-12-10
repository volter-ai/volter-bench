from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, create_from_game_database
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]
        
        # Initialize action storage
        self.current_player_action = None
        self.current_opponent_action = None
        self.battle_ended = False

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Opponent's {self.opponent.active_creature.display_name}: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp} HP

> Attack
> Swap"""

    def reset_creatures_state(self, player):
        """Reset creatures to their original prototype state"""
        fresh_creatures = []
        for creature in player.creatures:
            fresh_creature = create_from_game_database(creature.prototype_id, Creature)
            fresh_creatures.append(fresh_creature)
        player.creatures = fresh_creatures
        player.active_creature = None

    def run(self):
        while not self.battle_ended:
            # Player turn
            if not self.get_player_action(self.player):
                continue
                
            # Opponent turn
            if not self.get_player_action(self.opponent):
                continue

            # Resolve actions
            self.resolve_turn(self.current_player_action, self.current_opponent_action)

            # Check for battle end
            self.check_battle_end()

    def get_player_action(self, player):
        if player.active_creature.hp <= 0:
            if not self.handle_knockout(player):
                return False
                
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            action = self.handle_attack_choice(player)
        else:
            action = self.handle_swap_choice(player)
            
        if action is None:
            return False
            
        if player == self.player:
            self.current_player_action = action
        else:
            self.current_opponent_action = action
        return True

    def handle_attack_choice(self, player):
        skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, skill_choices + [back_button])
        
        if choice == back_button:
            return None
            
        return {"type": "attack", "skill": choice.thing}

    def handle_swap_choice(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, creature_choices + [back_button])
        
        if choice == back_button:
            return None
            
        return {"type": "swap", "creature": choice.thing}

    def handle_knockout(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if not available_creatures:
            self._show_text(self.player, f"{player.display_name} has no creatures left!")
            return False
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        return True

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"You switched to {player_action['creature'].display_name}!")
            
        if opponent_action["type"] == "swap":
            self.opponent.active_creature = opponent_action["creature"]
            self._show_text(self.player, f"Opponent switched to {opponent_action['creature'].display_name}!")

        # Then handle attacks
        first, second = self.determine_order(player_action, opponent_action)
        self.execute_action(first)
        self.execute_action(second)

    def determine_order(self, player_action, opponent_action):
        if player_action["type"] == "swap" or opponent_action["type"] == "swap":
            return player_action, opponent_action
            
        if self.player.active_creature.speed > self.opponent.active_creature.speed:
            return player_action, opponent_action
        elif self.player.active_creature.speed < self.opponent.active_creature.speed:
            return opponent_action, player_action
        else:
            if random.random() < 0.5:
                return player_action, opponent_action
            return opponent_action, player_action

    def execute_action(self, action):
        if action["type"] != "attack":
            return
            
        # Compare action to stored actions to determine attacker
        attacker = self.player if action is self.current_player_action else self.opponent
        defender = self.opponent if action is self.current_player_action else self.player
        
        skill = action["skill"]
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name}! Dealt {damage} damage!")

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        opponent_alive = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_alive:
            self._show_text(self.player, "You lost the battle!")
            self.battle_ended = True
            # Reset creature states before ending
            self.reset_creatures_state(self.player)
            self.reset_creatures_state(self.opponent)
            self._quit_whole_game()
        elif not opponent_alive:
            self._show_text(self.player, "You won the battle!")
            self.battle_ended = True
            # Reset creature states before ending
            self.reset_creatures_state(self.player)
            self.reset_creatures_state(self.opponent)
            self._quit_whole_game()
