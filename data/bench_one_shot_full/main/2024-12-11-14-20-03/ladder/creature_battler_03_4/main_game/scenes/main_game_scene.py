from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
Your {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
Opponent's {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{self._format_skills()}
"""

    def _format_skills(self):
        return "\n".join([f"> {skill.display_name} ({skill.skill_type} type)" 
                         for skill in self.player_creature.skills])

    def _calculate_damage(self, attacker_creature, defender_creature, skill):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        # Type effectiveness
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf": multiplier = 2.0
            elif defender_creature.creature_type == "water": multiplier = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire": multiplier = 2.0
            elif defender_creature.creature_type == "leaf": multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water": multiplier = 2.0
            elif defender_creature.creature_type == "fire": multiplier = 0.5

        return int(raw_damage * multiplier)

    def run(self):
        while True:
            # Player choice phase
            choices = [SelectThing(skill) for skill in self.player_creature.skills]
            self.player_chosen_skill = self._wait_for_choice(self.player, choices).thing

            # Opponent choice phase
            opponent_choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
            self.opponent_chosen_skill = self._wait_for_choice(self.opponent, opponent_choices).thing

            # Resolution phase
            first = self.player_creature
            second = self.opponent_creature
            first_skill = self.player_chosen_skill
            second_skill = self.opponent_chosen_skill

            if self.opponent_creature.speed > self.player_creature.speed or \
               (self.opponent_creature.speed == self.player_creature.speed and random.random() < 0.5):
                first, second = second, first
                first_skill, second_skill = second_skill, first_skill

            # First attack
            damage = self._calculate_damage(first, second, first_skill)
            second.hp -= damage
            self._show_text(self.player, f"{first.display_name} used {first_skill.display_name} for {damage} damage!")
            
            if second.hp <= 0:
                winner = "You" if second == self.opponent_creature else "Opponent"
                self._show_text(self.player, f"{winner} won the battle!")
                self._transition_to_scene("MainMenuScene")
                return

            # Second attack
            damage = self._calculate_damage(second, first, second_skill)
            first.hp -= damage
            self._show_text(self.player, f"{second.display_name} used {second_skill.display_name} for {damage} damage!")

            if first.hp <= 0:
                winner = "You" if first == self.opponent_creature else "Opponent"
                self._show_text(self.player, f"{winner} won the battle!")
                self._transition_to_scene("MainMenuScene")
                return
