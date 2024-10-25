from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Skill
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

Your turn! Choose a skill:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self.battle_loop()
        self.end_battle()

    def battle_loop(self):
        while True:
            player_skill = self.player_choice_phase()
            opponent_skill = self.opponent_choice_phase()
            self.resolution_phase(player_skill, opponent_skill)
            
            if self.check_battle_end():
                break

    def player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def opponent_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def resolution_phase(self, player_skill: Skill, opponent_skill: Skill):
        first, second = self.determine_order()
        self.execute_skill(first, second, player_skill if first == self.player else opponent_skill)
        if not self.check_battle_end():
            self.execute_skill(second, first, opponent_skill if first == self.player else player_skill)

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return self.player, self.opponent
        elif self.player_creature.speed < self.opponent_creature.speed:
            return self.opponent, self.player
        else:
            return random.sample([self.player, self.opponent], 2)

    def execute_skill(self, attacker: Player, defender: Player, skill: Skill):
        attacker_creature = attacker.creatures[0]
        defender_creature = defender.creatures[0]
        damage = max(0, attacker_creature.attack + skill.base_damage - defender_creature.defense)
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")

    def check_battle_end(self):
        return self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0

    def end_battle(self):
        if self.player_creature.hp <= 0:
            result = f"{self.player_creature.display_name} fainted! You lose!"
        else:
            result = f"{self.opponent_creature.display_name} fainted! You win!"
        
        self._show_text(self.player, result)
        self._show_text(self.player, "Returning to main menu...")
        self._transition_to_scene("MainMenuScene")
