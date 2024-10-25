from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

> Choose a skill
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        while True:
            player_skill = self._player_turn()
            opponent_skill = self._opponent_turn()
            self._resolve_turn(player_skill, opponent_skill)
            
            if self._check_battle_end():
                break

    def _player_turn(self):
        self._show_text(self.player, "Your turn!")
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _opponent_turn(self):
        self._show_text(self.opponent, "Opponent's turn!")
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _resolve_turn(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self._execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self._execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self._execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
            if self.player_creature.hp > 0:
                self._execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
        else:
            # Equal speed, randomly decide who goes first
            if random.choice([True, False]):
                self._execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
                if self.opponent_creature.hp > 0:
                    self._execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
            else:
                self._execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
                if self.player_creature.hp > 0:
                    self._execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)

    def _execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        weakness_factor = self._calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * weakness_factor)
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"{defender_creature.display_name} took {final_damage} damage!")

    def _calculate_weakness_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1  # Normal type is neither effective nor ineffective against any type
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

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._end_battle()
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._end_battle()
            return True
        return False

    def _end_battle(self):
        self._show_text(self.player, "Returning to main menu...")
        self._transition_to_scene("MainMenuScene")
