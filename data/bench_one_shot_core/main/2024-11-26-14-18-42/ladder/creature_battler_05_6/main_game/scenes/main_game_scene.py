from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
        player_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP" 
            for c in self.player.creatures
        )
        opponent_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP"
            for c in self.opponent.creatures
        )
        
        return f"""=== Battle ===
Your Active: {self.player.active_creature.display_name} ({self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP)
Opponent's Active: {self.opponent.active_creature.display_name} ({self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp} HP)

Your Team:
{player_creatures_status}

Opponent's Team:
{opponent_creatures_status}"""

    def run(self):
        while True:
            # Check for knocked out creatures and force swaps
            if self.player.active_creature.hp <= 0:
                if not self.handle_forced_swap(self.player):
                    self.end_battle(self.opponent)
                    return
            if self.opponent.active_creature.hp <= 0:
                if not self.handle_forced_swap(self.opponent):
                    self.end_battle(self.player)
                    return

            # Get actions with back button support
            player_action = self.get_turn_action_with_back(self.player)
            opponent_action = self.get_turn_action_with_back(self.opponent)
            
            # Resolve actions in proper order
            self.resolve_turn_with_speed(player_action, opponent_action)
            
            # Check for battle end
            winner = self.check_battle_end()
            if winner:
                self.end_battle(winner)
                return

    def get_turn_action_with_back(self, player):
        while True:
            # Main choice
            choices = [Button("Attack")]
            if self.get_available_creatures(player):
                choices.append(Button("Swap"))
            
            main_choice = self._wait_for_choice(player, choices)
            
            if main_choice.display_name == "Attack":
                # Show skills with back option
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(Button("Back"))
                
                choice = self._wait_for_choice(player, skill_choices)
                if choice.display_name == "Back":
                    continue
                return choice
            else:
                # Show creatures with back option
                available_creatures = self.get_available_creatures(player)
                creature_choices = [SelectThing(c) for c in available_creatures]
                creature_choices.append(Button("Back"))
                
                choice = self._wait_for_choice(player, creature_choices)
                if choice.display_name == "Back":
                    continue
                return choice

    def resolve_turn_with_speed(self, player_action, opponent_action):
        # Handle swaps first (they always go before attacks)
        swaps = []
        attacks = []
        
        if isinstance(player_action.thing, Creature):
            swaps.append((self.player, player_action))
        else:
            attacks.append((self.player, player_action))
            
        if isinstance(opponent_action.thing, Creature):
            swaps.append((self.opponent, opponent_action))
        else:
            attacks.append((self.opponent, opponent_action))
            
        # Execute all swaps first
        for player, action in swaps:
            if player == self.player:
                self.player.active_creature = action.thing
            else:
                self.opponent.active_creature = action.thing
                
        # Then execute attacks in speed order
        if len(attacks) == 2:
            # Both players used attacks - determine order by speed
            player1, action1 = attacks[0]
            player2, action2 = attacks[1]
            
            speed1 = player1.active_creature.speed
            speed2 = player2.active_creature.speed
            
            if speed1 > speed2:
                ordered_attacks = attacks
            elif speed2 > speed1:
                ordered_attacks = [attacks[1], attacks[0]]
            else:
                # Speed tie - random order
                ordered_attacks = list(attacks)
                random.shuffle(ordered_attacks)
                
            # Execute attacks in determined order
            for attacker, action in ordered_attacks:
                if attacker.active_creature.hp > 0:  # Only attack if still conscious
                    self.resolve_attack(attacker, 
                                     self.opponent if attacker == self.player else self.player,
                                     action.thing)
        
        elif len(attacks) == 1:
            # Only one attack - execute it
            attacker, action = attacks[0]
            self.resolve_attack(attacker,
                              self.opponent if attacker == self.player else self.player,
                              action.thing)

    def end_battle(self, winner):
        if winner == self.player:
            self._show_text(self.player, "You won the battle!")
        else:
            self._show_text(self.player, "You lost the battle!")
            
        # Reset creature HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
            
        self._quit_whole_game()

    def get_available_creatures(self, player):
        return [
            c for c in player.creatures 
            if c != player.active_creature and c.hp > 0
        ]

    def handle_forced_swap(self, player):
        available = self.get_available_creatures(player)
        if not available:
            return False
            
        creature_choices = [SelectThing(c) for c in available]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        return True

    def resolve_attack(self, attacker, defender, skill):
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
            
        multiplier = self.get_type_multiplier(
            skill.skill_type, 
            defender.active_creature.creature_type
        )
        
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(
            attacker,
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage!"
        )

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
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        opponent_has_creatures = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_has_creatures:
            return self.opponent
        elif not opponent_has_creatures:
            return self.player
            
        return None
