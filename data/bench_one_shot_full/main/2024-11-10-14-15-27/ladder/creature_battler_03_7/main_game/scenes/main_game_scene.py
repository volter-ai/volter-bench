from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._handle_player_turn()
            
            # Opponent Choice Phase  
            opponent_skill = self._handle_opponent_turn()
            
            # Resolution Phase
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost the battle!")
                self._transition_to_scene("MainMenuScene")  # Return to menu after battle
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won the battle!")
                self._transition_to_scene("MainMenuScene")  # Return to menu after battle

    def _handle_player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _handle_opponent_turn(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _calculate_damage(self, attacker, skill, defender):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Type effectiveness
        factor = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": factor = 2.0
            elif defender.creature_type == "water": factor = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": factor = 2.0
            elif defender.creature_type == "leaf": factor = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": factor = 2.0
            elif defender.creature_type == "fire": factor = 0.5
            
        return int(raw_damage * factor)

    def _resolve_turn(self, player_skill, opponent_skill):
        # Determine order
        first = self.player_creature if self.player_creature.speed > self.opponent_creature.speed else self.opponent_creature
        second = self.opponent_creature if first == self.player_creature else self.player_creature
        first_skill = player_skill if first == self.player_creature else opponent_skill
        second_skill = opponent_skill if first == self.player_creature else player_skill
        
        # If speeds are equal, randomize
        if self.player_creature.speed == self.opponent_creature.speed:
            if random.random() < 0.5:
                first, second = second, first
                first_skill, second_skill = second_skill, first_skill

        # Execute skills
        for attacker, defender, skill in [(first, second, first_skill), (second, first, second_skill)]:
            if defender.hp > 0:  # Only attack if defender still alive
                damage = self._calculate_damage(attacker, skill, defender)
                defender.hp = max(0, defender.hp - damage)
                self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")
