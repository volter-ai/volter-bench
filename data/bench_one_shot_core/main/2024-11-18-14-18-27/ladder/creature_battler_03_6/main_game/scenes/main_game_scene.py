from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_chosen_skill = None
        self.opponent_chosen_skill = None

    def __str__(self):
        return f"""=== Battle Scene ===
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Opponent's {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name} ({skill.skill_type} type, {skill.base_damage} damage)" 
                         for skill in skills])

    def _calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Type effectiveness
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": multiplier = 2.0
            elif defender.creature_type == "water": multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": multiplier = 2.0
            elif defender.creature_type == "leaf": multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": multiplier = 2.0
            elif defender.creature_type == "fire": multiplier = 0.5

        return int(raw_damage * multiplier)

    def _execute_turn(self):
        # Determine order
        first = self.player
        second = self.opponent
        first_creature = self.player_creature
        second_creature = self.opponent_creature
        first_skill = self.player_chosen_skill
        second_skill = self.opponent_chosen_skill

        if second_creature.speed > first_creature.speed or \
           (second_creature.speed == first_creature.speed and random.random() < 0.5):
            first, second = second, first
            first_creature, second_creature = second_creature, first_creature
            first_skill, second_skill = second_skill, first_skill

        # Execute skills
        for attacker, defender, skill, creature, target in [
            (first, second, first_skill, first_creature, second_creature),
            (second, first, second_skill, second_creature, first_creature)
        ]:
            if target.hp <= 0:
                continue
                
            damage = self._calculate_damage(creature, target, skill)
            target.hp = max(0, target.hp - damage)
            
            self._show_text(self.player, 
                f"{creature.display_name} used {skill.display_name}! "
                f"Dealt {damage} damage to {target.display_name}!")

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")

        while True:
            # Player choice phase
            skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            self.player_chosen_skill = self._wait_for_choice(self.player, skill_choices).thing

            # Opponent choice phase
            opponent_skills = [SelectThing(skill) for skill in self.opponent_creature.skills]
            self.opponent_chosen_skill = self._wait_for_choice(self.opponent, opponent_skills).thing

            # Resolution phase
            self._execute_turn()

            # Check win condition
            if self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
            elif self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break

        self._transition_to_scene("MainMenuScene")
