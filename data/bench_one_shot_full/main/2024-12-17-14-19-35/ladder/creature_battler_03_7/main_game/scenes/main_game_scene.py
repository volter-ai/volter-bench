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
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player choice phase
            self.player_chosen_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent choice phase
            self.opponent_chosen_skill = self._get_skill_choice(self.opponent, self.opponent_creature)
            
            # Resolution phase
            first, second = self._determine_turn_order()
            
            # Execute moves
            if not self._execute_skill(first[0], first[1], first[2], first[3]):
                break
                
            if not self._execute_skill(second[0], second[1], second[2], second[3]):
                break

    def _get_skill_choice(self, actor, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(actor, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _determine_turn_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            first = (self.player, self.player_creature, self.player_chosen_skill, self.opponent_creature)
            second = (self.opponent, self.opponent_creature, self.opponent_chosen_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            first = (self.opponent, self.opponent_creature, self.opponent_chosen_skill, self.player_creature)
            second = (self.player, self.player_creature, self.player_chosen_skill, self.opponent_creature)
        else:
            actors = [(self.player, self.player_creature, self.player_chosen_skill, self.opponent_creature),
                     (self.opponent, self.opponent_creature, self.opponent_chosen_skill, self.player_creature)]
            random.shuffle(actors)
            first, second = actors
        return first, second

    def _execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        # Calculate raw damage
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        # Calculate type multiplier
        multiplier = self._get_type_multiplier(skill.skill_type, defender_creature.creature_type)
        
        # Calculate final damage
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        # Show result
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"Dealt {final_damage} damage!")
        
        # Check if battle is over
        if defender_creature.hp <= 0:
            winner = attacker.display_name
            self._show_text(self.player, f"{winner} wins!")
            self._transition_to_scene("MainMenuScene")
            return False
            
        return True

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
