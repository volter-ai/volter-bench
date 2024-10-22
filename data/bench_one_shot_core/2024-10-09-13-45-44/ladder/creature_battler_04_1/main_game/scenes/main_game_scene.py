import random

from main_game.models import Creature, Skill
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Player's turn:
> {self.player_creature.skills[0].display_name}
> {self.player_creature.skills[1].display_name}

Opponent's skills:
> {self.opponent_creature.skills[0].display_name}
> {self.opponent_creature.skills[1].display_name}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        while True:
            player_skill = self.player_turn()
            opponent_skill = self.opponent_turn()
            
            if self.player_creature.speed > self.opponent_creature.speed:
                self.execute_skill(self.player_creature, self.opponent_creature, player_skill)
                if self.check_battle_end():
                    break
                self.execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
            elif self.player_creature.speed < self.opponent_creature.speed:
                self.execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
                if self.check_battle_end():
                    break
                self.execute_skill(self.player_creature, self.opponent_creature, player_skill)
            else:
                # Same speed, random order
                if random.choice([True, False]):
                    self.execute_skill(self.player_creature, self.opponent_creature, player_skill)
                    if self.check_battle_end():
                        break
                    self.execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
                else:
                    self.execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
                    if self.check_battle_end():
                        break
                    self.execute_skill(self.player_creature, self.opponent_creature, player_skill)
            
            if self.check_battle_end():
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        self._show_text(self.player, f"It's your turn! Choose a skill for {self.player_creature.display_name}:")
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_turn(self):
        self._show_text(self.player, f"Opponent's turn! {self.opponent_creature.display_name}'s available skills:")
        for skill in self.opponent_creature.skills:
            self._show_text(self.player, f"- {skill.display_name}")
        
        opponent_skill = random.choice(self.opponent_creature.skills)
        self._show_text(self.player, f"{self.opponent_creature.display_name} uses {opponent_skill.display_name}!")
        return opponent_skill

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_factor * raw_damage)

        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")

    def calculate_weakness_factor(self, skill_type: str, defender_type: str):
        if skill_type == "normal":
            return 1
        elif skill_type == defender_type:
            return 1
        elif (skill_type == "fire" and defender_type == "leaf") or \
             (skill_type == "water" and defender_type == "fire") or \
             (skill_type == "leaf" and defender_type == "water"):
            return 2
        elif (skill_type == "fire" and defender_type == "water") or \
             (skill_type == "water" and defender_type == "leaf") or \
             (skill_type == "leaf" and defender_type == "fire"):
            return 0.5
        else:
            return 1

    def check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lost the battle.")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"{self.opponent_creature.display_name} fainted! You won the battle!")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
