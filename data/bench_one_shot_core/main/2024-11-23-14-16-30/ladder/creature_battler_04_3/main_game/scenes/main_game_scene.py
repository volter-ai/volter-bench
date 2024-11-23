from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        
    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        while True:
            # Player phase
            player_skill = self._handle_player_turn()
            
            # Opponent phase  
            opponent_skill = self._handle_opponent_turn()
            
            # Resolution phase
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check win condition
            if self._check_battle_end():
                # Reset creature states before transitioning
                self._reset_creature_states()
                # Return to main menu
                self._transition_to_scene("MainMenuScene")
                return

    def _reset_creature_states(self):
        """Reset all creatures to their initial state"""
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def _handle_player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _handle_opponent_turn(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Calculate type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def _get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"water": 0.5, "leaf": 2.0},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def _resolve_turn(self, player_skill, opponent_skill):
        # Determine order
        first, second = self._determine_order(
            (self.player_creature, player_skill, self.opponent_creature),
            (self.opponent_creature, opponent_skill, self.player_creature)
        )
        
        # Execute moves in order
        for attacker, skill, defender in [first, second]:
            damage = self._calculate_damage(attacker, defender, skill)
            defender.hp = max(0, defender.hp - damage)
            
            self._show_text(self.player, 
                f"{attacker.display_name} used {skill.display_name}! Dealt {damage} damage!")
            
            if defender.hp == 0:
                break

    def _determine_order(self, player_data, opponent_data):
        if player_data[0].speed > opponent_data[0].speed:
            return player_data, opponent_data
        elif player_data[0].speed < opponent_data[0].speed:
            return opponent_data, player_data
        else:
            if random.random() < 0.5:
                return player_data, opponent_data
            return opponent_data, player_data

    def _check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
