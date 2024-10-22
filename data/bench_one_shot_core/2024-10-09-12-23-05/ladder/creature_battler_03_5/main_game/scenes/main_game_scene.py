import random

from mini_game_engine.engine.lib import AbstractGameScene, Button


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

Your turn! Choose a skill:
{self._get_skill_choices_str()}
"""

    def _get_skill_choices_str(self):
        return "\n".join([f"> {skill.display_name}" for skill in self.player_creature.skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self.game_loop()

    def game_loop(self):
        while True:
            player_skill = self._player_turn()
            opponent_skill = self._opponent_turn()

            first, second = self._determine_turn_order(player_skill, opponent_skill)
            self._resolve_turn(first)
            if self._check_battle_end():
                break
            self._resolve_turn(second)
            if self._check_battle_end():
                break

    def _player_turn(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _opponent_turn(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def _determine_turn_order(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, player_skill), (self.opponent, opponent_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, opponent_skill), (self.player, player_skill)
        else:
            if random.random() < 0.5:
                return (self.player, player_skill), (self.opponent, opponent_skill)
            else:
                return (self.opponent, opponent_skill), (self.player, player_skill)

    def _resolve_turn(self, turn):
        attacker, skill = turn
        if attacker == self.player:
            attacker_creature = self.player_creature
            defender_creature = self.opponent_creature
        else:
            attacker_creature = self.opponent_creature
            defender_creature = self.player_creature

        damage = self._calculate_damage(attacker_creature, defender_creature, skill)
        defender_creature.hp = max(0, defender_creature.hp - damage)

        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")

    def _calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_factor)

    def _get_type_factor(self, skill_type, defender_type):
        if skill_type == defender_type:
            return 1  # Same type, normal damage
        elif skill_type == "normal":
            return 1  # Normal type, always normal damage
        elif skill_type == "fire":
            if defender_type == "leaf":
                return 2
            elif defender_type == "water":
                return 0.5
        elif skill_type == "water":
            if defender_type == "fire":
                return 2
            elif defender_type == "leaf":
                return 0.5
        elif skill_type == "leaf":
            if defender_type == "water":
                return 2
            elif defender_type == "fire":
                return 0.5
        return 1  # Default case, normal damage

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent_creature.display_name} fainted! You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
