from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_chosen_skill = None
        self.opponent_chosen_skill = None

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} - {skill.base_damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player choice phase
            self.player_chosen_skill = self._handle_player_turn(self.player, self.player_creature)
            
            # Opponent choice phase
            self.opponent_chosen_skill = self._handle_player_turn(self.opponent, self.opponent_creature)
            
            # Resolution phase
            self._resolve_turn()
            
            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
        
        self._transition_to_scene("MainMenuScene")

    def _handle_player_turn(self, current_player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolve_turn(self):
        # Determine order based on speed
        first = self.player
        second = self.opponent
        first_skill = self.player_chosen_skill
        second_skill = self.opponent_chosen_skill
        
        if self.opponent_creature.speed > self.player_creature.speed or \
           (self.opponent_creature.speed == self.player_creature.speed and random.random() < 0.5):
            first, second = second, first
            first_skill, second_skill = second_skill, first_skill
        
        # Execute skills in order
        self._execute_skill(first_skill, 
                          self.player_creature if first == self.player else self.opponent_creature,
                          self.opponent_creature if first == self.player else self.player_creature)
        
        if self.player_creature.hp > 0 and self.opponent_creature.hp > 0:
            self._execute_skill(second_skill,
                              self.player_creature if second == self.player else self.opponent_creature,
                              self.opponent_creature if second == self.player else self.player_creature)

    def _execute_skill(self, skill, attacker, defender):
        # Calculate raw damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, 
                       f"{attacker.display_name} used {skill.display_name}! "
                       f"Dealt {final_damage} damage to {defender.display_name}")

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
