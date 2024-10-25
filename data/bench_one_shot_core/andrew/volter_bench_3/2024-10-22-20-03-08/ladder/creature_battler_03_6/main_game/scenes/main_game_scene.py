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
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._player_choice_phase(self.player, self.player_creature)
            
            # Foe Choice Phase
            foe_skill = self._player_choice_phase(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self._resolution_phase(player_skill, foe_skill)
            
            if self._check_battle_end():
                self._handle_battle_end()
                break

    def _player_choice_phase(self, current_player, current_creature):
        choices = [Button(skill.display_name) for skill in current_creature.skills]
        choice = self._wait_for_choice(current_player, choices)
        return next(skill for skill in current_creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill, foe_skill):
        first, second = self._determine_order(self.player_creature, self.opponent_creature)
        first_skill = player_skill if first == self.player_creature else foe_skill
        second_skill = foe_skill if first == self.player_creature else player_skill

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
        weakness_factor = self._get_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender.hp = max(0, defender.hp - final_damage)

        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")

    def _get_weakness_factor(self, skill_type, defender_type):
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
        return self.player_creature.hp <= 0 or self.opponent_creature.hp <= 0

    def _handle_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}, you have lost the battle!")
        else:
            self._show_text(self.player, f"Congratulations {self.player.display_name}, you have won the battle!")

        choices = [Button("Return to Main Menu"), Button("Quit Game")]
        choice = self._wait_for_choice(self.player, choices)

        if choice.display_name == "Return to Main Menu":
            self._transition_to_scene("MainMenuScene")
        else:
            self._quit_whole_game()
