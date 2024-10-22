from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature, Skill
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
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while True:
            if self.battle_round():
                break

    def battle_round(self):
        # Player Choice Phase
        player_skill = self.player_choice_phase()

        # Foe Choice Phase
        opponent_skill = self.foe_choice_phase()

        # Resolution Phase
        return self.resolution_phase(player_skill, opponent_skill)

    def player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def foe_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def resolution_phase(self, player_skill: Skill, opponent_skill: Skill):
        first, second = self.determine_order()
        
        if self.execute_skill(first[0], first[1], second[0], second[1]):
            return True
        if self.execute_skill(second[0], second[1], first[0], first[1]):
            return True
        
        return False

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_creature), (self.opponent, self.opponent_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.opponent_creature), (self.player, self.player_creature)
        else:
            if random.choice([True, False]):
                return (self.player, self.player_creature), (self.opponent, self.opponent_creature)
            else:
                return (self.opponent, self.opponent_creature), (self.player, self.player_creature)

    def execute_skill(self, attacker: Player, attacker_creature: Creature, defender: Player, defender_creature: Creature):
        damage = attacker_creature.attack + attacker_creature.skills[0].base_damage - defender_creature.defense
        defender_creature.hp = max(0, defender_creature.hp - damage)
        
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} used {attacker_creature.skills[0].display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} took {damage} damage!")
        
        if defender_creature.hp == 0:
            self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} fainted!")
            if defender == self.player:
                self._show_text(self.player, "You lost the battle!")
            else:
                self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        
        return False
