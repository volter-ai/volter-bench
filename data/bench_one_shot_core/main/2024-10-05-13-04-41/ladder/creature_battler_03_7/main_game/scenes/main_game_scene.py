from mini_game_engine.engine.lib import AbstractGameScene, Button
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.current_turn = 0

    def __str__(self):
        return f"""===Battle===
Turn: {self.current_turn}

{self.player.display_name}'s {self.player_creature.display_name}:
HP: {self.player_creature.hp}/{self.player_creature.max_hp}

{self.opponent.display_name}'s {self.opponent_creature.display_name}:
HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        while True:
            self.current_turn += 1
            player_skill = self._player_choice_phase()
            opponent_skill = self._opponent_choice_phase()
            self._resolution_phase(player_skill, opponent_skill)
            
            if self._check_battle_end():
                break

    def _player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _opponent_choice_phase(self):
        return self._wait_for_choice(self.opponent, self.opponent_creature.skills)

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
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        weakness_factor = self._calculate_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * weakness_factor)
        defender.hp = max(0, defender.hp - final_damage)

        attacker_name = self.player.display_name if attacker == self.player_creature else self.opponent.display_name
        defender_name = self.opponent.display_name if attacker == self.player_creature else self.player.display_name
        self._show_text(self.player, f"{attacker_name}'s {attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_name}'s {defender.display_name} took {final_damage} damage!")

    def _calculate_weakness_factor(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("water", "fire"): 2,
            ("leaf", "water"): 2,
            ("fire", "water"): 0.5,
            ("water", "leaf"): 0.5,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._end_battle(f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._end_battle(f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            return True
        return False

    def _end_battle(self, message):
        self._show_text(self.player, message)
        self._transition_to_scene("MainMenuScene")
