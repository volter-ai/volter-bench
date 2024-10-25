from mini_game_engine.engine.lib import AbstractGameScene, Button
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, "A wild opponent appears!")
        self.game_loop()
        self._reset_player_creatures()
        self._transition_to_scene("MainMenuScene")

    def game_loop(self):
        while self.player_creature.hp > 0 and self.opponent_creature.hp > 0:
            player_skill = self._player_choice_phase()
            opponent_skill = self._foe_choice_phase()
            self._resolution_phase(player_skill, opponent_skill)

        self._show_battle_result()

    def _player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _foe_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill, opponent_skill):
        first, second = self._determine_order(self.player_creature, self.opponent_creature)
        first_skill = player_skill if first == self.player_creature else opponent_skill
        second_skill = opponent_skill if first == self.player_creature else player_skill

        self._execute_skill(first, second, first_skill)
        if second.hp > 0:
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
        self._show_text(self.player, f"{attacker.display_name} uses {skill.display_name} and deals {damage} damage to {defender.display_name}!")

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        else:
            raw_damage = float(attacker.sp_attack) / float(defender.sp_defense) * float(skill.base_damage)

        weakness_factor = self._get_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = weakness_factor * raw_damage
        return int(final_damage)  # Explicitly convert to integer as final step

    def _get_weakness_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        elif skill_type == "fire":
            if defender_type == "leaf":
                return 2.0
            elif defender_type == "water":
                return 0.5
        elif skill_type == "water":
            if defender_type == "fire":
                return 2.0
            elif defender_type == "leaf":
                return 0.5
        elif skill_type == "leaf":
            if defender_type == "water":
                return 2.0
            elif defender_type == "fire":
                return 0.5
        return 1.0  # Default case for no weakness or resistance

    def _show_battle_result(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")

    def _reset_player_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
