from mini_game_engine.engine.lib import AbstractGameScene, Button
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self.battle_loop()

    def battle_loop(self):
        while True:
            player_skill = self._player_turn()
            opponent_skill = self._opponent_turn()

            first, second = self._determine_turn_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            self._resolve_turn(*first)
            if self._check_battle_end():
                break

            self._resolve_turn(*second)
            if self._check_battle_end():
                break

    def _player_turn(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _opponent_turn(self):
        return random.choice(self.opponent_creature.skills)

    def _determine_turn_order(self, player_data, opponent_data):
        if player_data[1].speed > opponent_data[1].speed:
            return player_data, opponent_data
        elif player_data[1].speed < opponent_data[1].speed:
            return opponent_data, player_data
        else:
            return random.sample([player_data, opponent_data], 2)

    def _resolve_turn(self, attacker, attacker_creature, skill):
        defender = self.opponent if attacker == self.player else self.player
        defender_creature = self.opponent_creature if attacker == self.player else self.player_creature

        damage = self._calculate_damage(attacker_creature, defender_creature, skill)
        defender_creature.hp = max(0, defender_creature.hp - damage)

        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")

    def _calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_factor)

    def _get_type_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1
        elif skill_type == "fire" and defender_type == "leaf":
            return 2
        elif skill_type == "fire" and defender_type == "water":
            return 0.5
        elif skill_type == "water" and defender_type == "fire":
            return 2
        elif skill_type == "water" and defender_type == "leaf":
            return 0.5
        elif skill_type == "leaf" and defender_type == "water":
            return 2
        elif skill_type == "leaf" and defender_type == "fire":
            return 0.5
        else:
            return 1

    def _check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
