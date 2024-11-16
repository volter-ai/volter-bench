from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
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
{' '.join([f'> {skill.display_name}' for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._handle_player_turn()
            
            # Opponent Choice Phase
            opponent_skill = self._handle_opponent_turn()
            
            # Resolution Phase
            first, second = self._determine_turn_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )
            
            # Execute skills in order
            for attacker, creature, skill in [first, second]:
                if creature.hp <= 0:
                    continue
                    
                target = self.opponent_creature if attacker == self.player else self.player_creature
                damage = self._calculate_damage(creature, target, skill)
                target.hp -= damage
                
                self._show_text(self.player, f"{creature.display_name} used {skill.display_name}!")
                self._show_text(self.player, f"Dealt {damage} damage to {target.display_name}!")
                
                if target.hp <= 0:
                    winner = self.player if attacker == self.player else self.opponent
                    self._show_text(self.player, f"{winner.display_name} wins!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def _handle_player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _handle_opponent_turn(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _determine_turn_order(self, player_data, opponent_data):
        if player_data[1].speed > opponent_data[1].speed:
            return player_data, opponent_data
        elif player_data[1].speed < opponent_data[1].speed:
            return opponent_data, player_data
        else:
            return random.choice([(player_data, opponent_data), (opponent_data, player_data)])

    def _calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Calculate type multiplier
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        # Calculate final damage
        final_damage = int(raw_damage * multiplier)
        return max(1, final_damage)  # Minimum 1 damage

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
