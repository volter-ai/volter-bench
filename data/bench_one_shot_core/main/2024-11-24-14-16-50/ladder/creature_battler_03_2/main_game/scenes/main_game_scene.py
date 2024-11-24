from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} type)" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player phase
            player_skill = self._handle_player_turn()
            
            # Opponent phase  
            opponent_skill = self._handle_opponent_turn()
            
            # Resolution phase
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check win condition
            if self.player_creature.hp == 0:
                self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lose!")
                self._transition_to_scene("MainMenuScene")
                return
            elif self.opponent_creature.hp == 0:
                self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} fainted! You win!")
                self._transition_to_scene("MainMenuScene")
                return

    def _handle_player_turn(self) -> Skill:
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _handle_opponent_turn(self) -> Skill:
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _calculate_damage(self, attacker_creature, defender_creature, skill):
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

    def _resolve_turn(self, player_skill, opponent_skill):
        # Determine order
        first = self.player
        second = self.opponent
        first_skill = player_skill
        second_skill = opponent_skill
        
        if self.opponent_creature.speed > self.player_creature.speed:
            first, second = second, first
            first_skill, second_skill = second_skill, first_skill
        
        # Execute skills
        for attacker, defender, skill in [(first, second, first_skill), (second, first, second_skill)]:
            attacker_creature = self.player_creature if attacker == self.player else self.opponent_creature
            defender_creature = self.opponent_creature if attacker == self.player else self.player_creature
            
            damage = self._calculate_damage(attacker_creature, defender_creature, skill)
            defender_creature.hp = max(0, defender_creature.hp - damage)
            
            self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name} for {damage} damage!")
            
            if defender_creature.hp == 0:
                break
