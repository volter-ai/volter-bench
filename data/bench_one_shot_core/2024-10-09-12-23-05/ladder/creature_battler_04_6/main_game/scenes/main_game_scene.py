from mini_game_engine.engine.lib import AbstractGameScene, Button
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

Your turn! Choose a skill:
{self._get_skill_choices_str()}
"""

    def _get_skill_choices_str(self):
        return "\n".join([f"> {skill.display_name}" for skill in self.player_creature.skills])

    def run(self):
        self._show_text(self.player, "Welcome to the battle! May the best creature win!")
        self.game_loop()

    def game_loop(self):
        while True:
            player_skill = self._player_choice_phase()
            opponent_skill = self._foe_choice_phase()
            self._resolution_phase(player_skill, opponent_skill)

            if self._check_battle_end():
                break

    def _player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _foe_choice_phase(self):
        return random.choice(self.opponent_creature.skills)

    def _resolution_phase(self, player_skill, opponent_skill):
        first, second = self._determine_order(self.player_creature, self.opponent_creature)
        first_skill = player_skill if first == self.player_creature else opponent_skill
        second_skill = opponent_skill if first == self.player_creature else player_skill

        self._execute_skill(first, second, first_skill)
        if not self._check_battle_end():
            self._execute_skill(second, first, second_skill)

    def _determine_order(self, creature1, creature2):
        if creature1.speed > creature2.speed:
            return creature1, creature2
        elif creature2.speed > creature1.speed:
            return creature2, creature1
        else:
            return random.sample([creature1, creature2], 2)

    def _execute_skill(self, attacker, defender, skill):
        damage = self._calculate_damage(attacker, defender, skill)
        defender.hp = max(0, defender.hp - damage)

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return final_damage

    def _get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "normal": {"normal": 1, "fire": 1, "water": 1, "leaf": 1},
            "fire": {"normal": 1, "fire": 0.5, "water": 0.5, "leaf": 2},
            "water": {"normal": 1, "fire": 2, "water": 0.5, "leaf": 0.5},
            "leaf": {"normal": 1, "fire": 0.5, "water": 2, "leaf": 0.5}
        }
        return effectiveness.get(skill_type.lower(), {}).get(defender_type.lower(), 1)

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._reset_player_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._reset_player_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def _reset_player_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
