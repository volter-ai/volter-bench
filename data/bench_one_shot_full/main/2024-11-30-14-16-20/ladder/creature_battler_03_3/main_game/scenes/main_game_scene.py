from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_choice = None
        self.opponent_choice = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} - {skill.base_damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player choice phase
            choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, choices)
            self.player_choice = next(s for s in self.player_creature.skills if s.display_name == player_choice.display_name)

            # Opponent choice phase
            opponent_choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
            opponent_choice = self._wait_for_choice(self.opponent, opponent_choices)
            self.opponent_choice = next(s for s in self.opponent_creature.skills if s.display_name == opponent_choice.display_name)

            # Resolution phase
            first, second = self.determine_order()
            
            # Execute moves
            self.execute_move(*first)
            if self.check_battle_end():
                break
                
            self.execute_move(*second)
            if self.check_battle_end():
                break

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return ((self.player, self.player_creature, self.player_choice), (self.opponent_creature)), \
                   ((self.opponent, self.opponent_creature, self.opponent_choice), (self.player_creature))
        elif self.opponent_creature.speed > self.player_creature.speed:
            return ((self.opponent, self.opponent_creature, self.opponent_choice), (self.player_creature)), \
                   ((self.player, self.player_creature, self.player_choice), (self.opponent_creature))
        else:
            moves = [
                ((self.player, self.player_creature, self.player_choice), (self.opponent_creature)),
                ((self.opponent, self.opponent_creature, self.opponent_choice), (self.player_creature))
            ]
            random.shuffle(moves)
            return moves[0], moves[1]

    def execute_move(self, attacker_info, target):
        owner, attacker, skill = attacker_info
        
        # Calculate raw damage using the creature's stats
        raw_damage = attacker.attack + skill.base_damage - target.defense
        
        # Apply type multiplier
        multiplier = self.get_type_multiplier(skill.skill_type, target.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        target.hp = max(0, target.hp - final_damage)
        
        self._show_text(self.player, f"{owner.display_name}'s {attacker.display_name} uses {skill.display_name} for {final_damage} damage!")

    def get_type_multiplier(self, skill_type, target_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(target_type, 1.0)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
