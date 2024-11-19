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
        self._show_text(self.player, f"Battle start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player choice phase
            self.player_chosen_skill = self.get_skill_choice(self.player, self.player_creature)
            
            # Opponent choice phase
            self.opponent_chosen_skill = self.get_skill_choice(self.opponent, self.opponent_creature)
            
            # Resolution phase
            self.resolve_turn()
            
            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")

    def get_skill_choice(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        final_damage = int(raw_damage * effectiveness)
        return max(1, final_damage)  # Minimum 1 damage

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness_chart = {
            "fire": {"water": 0.5, "leaf": 2.0},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def resolve_turn(self):
        # Determine order based on creature speed
        first_creature = self.player_creature
        second_creature = self.opponent_creature
        first_skill = self.player_chosen_skill
        second_skill = self.opponent_chosen_skill
        
        # Swap if opponent is faster or equal speed with 50% chance
        if self.opponent_creature.speed > self.player_creature.speed or \
           (self.opponent_creature.speed == self.player_creature.speed and random.random() < 0.5):
            first_creature, second_creature = second_creature, first_creature
            first_skill, second_skill = second_skill, first_skill

        # Execute moves
        for attacker, defender, skill in [
            (first_creature, second_creature, first_skill),
            (second_creature, first_creature, second_skill)
        ]:
            if defender.hp > 0:  # Only attack if defender still alive
                damage = self.calculate_damage(attacker, defender, skill)
                defender.hp = max(0, defender.hp - damage)
                self._show_text(self.player, 
                    f"{attacker.display_name} used {skill.display_name}! "
                    f"Dealt {damage} damage to {defender.display_name}")
