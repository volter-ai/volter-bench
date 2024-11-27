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

    def __str__(self):
        p_creature = self.player.active_creature
        o_creature = self.opponent.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {o_creature.display_name}: {o_creature.hp}/{o_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue
                
            # Opponent turn
            opponent_action = self.get_player_action(self.opponent)
            if not opponent_action:
                continue
                
            # Resolve actions
            self.resolve_turn(player_action, opponent_action)
            
            # Check for battle end
            self.check_battle_end()

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self._wait_for_choice(player, 
                [SelectThing(skill) for skill in player.active_creature.skills])
        else:
            available_creatures = [c for c in player.creatures 
                                 if c != player.active_creature and c.hp > 0]
            if not available_creatures:
                self._show_text(player, "No other creatures available!")
                return None
                
            return self._wait_for_choice(player,
                [SelectThing(creature) for creature in available_creatures])

    def resolve_turn(self, player_action, opponent_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(opponent_action.thing, Creature):
            self.opponent.active_creature = opponent_action.thing
            
        # Determine order for attacks
        first, second = self.get_action_order(player_action, opponent_action)
        
        # Execute attacks
        if isinstance(first.thing, Skill):
            self.execute_attack(first.thing, 
                              first == player_action and self.player or self.opponent,
                              first != player_action and self.player or self.opponent)
            
        if isinstance(second.thing, Skill):
            self.execute_attack(second.thing,
                              second == player_action and self.player or self.opponent,
                              second != player_action and self.player or self.opponent)

    def execute_attack(self, skill, attacker, defender):
        # Calculate damage
        raw_damage = self.calculate_raw_damage(skill, attacker.active_creature, 
                                             defender.active_creature)
        
        # Apply type effectiveness
        final_damage = int(raw_damage * self.get_type_effectiveness(
            skill.skill_type, defender.active_creature.creature_type))
        
        # Apply damage
        defender.active_creature.hp = max(0, 
            defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, 
            f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender,
            f"It dealt {final_damage} damage!")

    def calculate_raw_damage(self, skill, attacker, defender):
        if skill.is_physical:
            return attacker.attack + skill.base_damage - defender.defense
        else:
            return (attacker.sp_attack / defender.sp_defense) * skill.base_damage

    def get_type_effectiveness(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def get_action_order(self, player_action, opponent_action):
        if isinstance(player_action.thing, Creature) or \
           isinstance(opponent_action.thing, Creature):
            return player_action, opponent_action
            
        if self.player.active_creature.speed > self.opponent.active_creature.speed:
            return player_action, opponent_action
        elif self.player.active_creature.speed < self.opponent.active_creature.speed:
            return opponent_action, player_action
        else:
            return random.choice([(player_action, opponent_action),
                                (opponent_action, player_action)])

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        opponent_has_creatures = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            self.reset_creatures()
            self._quit_whole_game()
        elif not opponent_has_creatures:
            self._show_text(self.player, "You won the battle!")
            self.reset_creatures()
            self._quit_whole_game()

    def reset_creatures(self):
        # Reset HP of all creatures to their max HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
