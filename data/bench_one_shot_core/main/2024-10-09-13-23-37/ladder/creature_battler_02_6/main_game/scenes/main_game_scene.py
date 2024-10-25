from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Player's turn:
{self.get_skill_choices_str(self.player_creature)}
"""

    def get_skill_choices_str(self, creature: Creature) -> str:
        return "\n".join([f"> {skill.display_name}" for skill in creature.skills])

    def run(self):
        self._show_text(self.player, "Welcome to the Creature Battle!")
        
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()
            
            # Foe Choice Phase
            opponent_skill = self.foe_choice_phase()
            
            # Resolution Phase
            self.resolution_phase(player_skill, opponent_skill)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def player_choice_phase(self) -> Skill:
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self) -> Skill:
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill: Skill, opponent_skill: Skill):
        if self.player_creature.speed > self.opponent_creature.speed or \
           (self.player_creature.speed == self.opponent_creature.speed and random.choice([True, False])):
            self.execute_skill(self.player_creature, player_skill, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self.execute_skill(self.opponent_creature, opponent_skill, self.player_creature)
        else:
            self.execute_skill(self.opponent_creature, opponent_skill, self.player_creature)
            if self.player_creature.hp > 0:
                self.execute_skill(self.player_creature, player_skill, self.opponent_creature)

    def execute_skill(self, attacker: Creature, skill: Skill, defender: Creature):
        damage = attacker.attack + skill.base_damage - defender.defense
        defender.hp = max(0, defender.hp - damage)

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            self._quit_whole_game()
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            self._quit_whole_game()
            return True
        return False
