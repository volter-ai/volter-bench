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
{self._format_creature_info(self.player, self.player_creature)}

{self._format_creature_info(self.opponent, self.opponent_creature)}
"""

    def _format_creature_info(self, player, creature):
        return f"""{player.display_name}: {creature.display_name} (HP: {creature.hp}/{creature.max_hp})
Available skills:
{self._format_skills(creature.skills)}"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        while True:
            player_skill = self._player_choice_phase()
            opponent_skill = self._foe_choice_phase()
            self._resolution_phase(player_skill, opponent_skill)

            if self._check_battle_end():
                self._show_battle_result()
                self._transition_to_scene("MainMenuScene")
                break

    def _player_choice_phase(self):
        self._show_text(self.player, f"It's {self.player.display_name}'s turn to choose a skill.")
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _foe_choice_phase(self):
        self._show_text(self.player, f"It's {self.opponent.display_name}'s turn to choose a skill.")
        self._show_text(self.player, f"{self.opponent.display_name}'s available skills:")
        self._show_text(self.player, self._format_skills(self.opponent_creature.skills))
        
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
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        weakness_factor = self._calculate_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender.hp = max(0, defender.hp - final_damage)

        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")

    def _calculate_weakness_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def _check_battle_end(self):
        return self.player_creature.hp == 0 or self.opponent_creature.hp == 0

    def _show_battle_result(self):
        if self.player_creature.hp == 0 and self.opponent_creature.hp == 0:
            self._show_text(self.player, "The battle ended in a draw!")
        elif self.player_creature.hp == 0:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
        else:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
        self._show_text(self.player, "Returning to the main menu...")
