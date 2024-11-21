from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
from dataclasses import dataclass
from typing import Optional

@dataclass
class QueuedAction:
    player_id: str
    skill: 'Skill'

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_queued_action: Optional[QueuedAction] = None
        self.opponent_queued_action: Optional[QueuedAction] = None

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} type)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.opponent, "Battle Start!")

        while True:
            # Player Choice Phase
            self.player_choice_phase()
            
            # Opponent Choice Phase  
            self.opponent_choice_phase()
            
            # Resolution Phase
            if self.resolution_phase():
                break

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_queued_action = QueuedAction(
            player_id=self.player.uid,
            skill=choice.thing
        )

    def opponent_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        self.opponent_queued_action = QueuedAction(
            player_id=self.opponent.uid,
            skill=choice.thing
        )

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        # Type effectiveness
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf":
                multiplier = 2.0
            elif defender_creature.creature_type == "water":
                multiplier = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire":
                multiplier = 2.0
            elif defender_creature.creature_type == "leaf":
                multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water":
                multiplier = 2.0
            elif defender_creature.creature_type == "fire":
                multiplier = 0.5

        return int(raw_damage * multiplier)

    def resolution_phase(self):
        # Determine order
        first_action = self.player_queued_action
        second_action = self.opponent_queued_action
        
        if self.opponent_creature.speed > self.player_creature.speed:
            first_action, second_action = second_action, first_action
        elif self.opponent_creature.speed == self.player_creature.speed:
            if random.random() < 0.5:
                first_action, second_action = second_action, first_action

        # Execute moves in order
        for action in [first_action, second_action]:
            is_player_action = action.player_id == self.player.uid
            attacker = self.player_creature if is_player_action else self.opponent_creature
            defender = self.opponent_creature if is_player_action else self.player_creature
            current_player = self.player if is_player_action else self.opponent
            skill = action.skill

            damage = self.calculate_damage(attacker, defender, skill)
            defender.hp = max(0, defender.hp - damage)

            self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")
            self._show_text(self.opponent, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")

            if defender.hp <= 0:
                winner = self.player if defender == self.opponent_creature else self.opponent
                self._show_text(self.player, f"{winner.display_name} wins!")
                self._show_text(self.opponent, f"{winner.display_name} wins!")
                self._transition_to_scene("MainMenuScene")
                return True

        self.player_queued_action = None
        self.opponent_queued_action = None
        return False
