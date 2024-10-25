from mini_game_engine.engine.lib import AbstractGameScene, Button, RandomModeGracefulExit
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
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
        try:
            self.game_loop()
        except RandomModeGracefulExit:
            self._transition_to_scene("MainMenuScene")

    def game_loop(self):
        while True:
            player_skill = self._player_choice_phase()
            opponent_skill = self._opponent_choice_phase()
            self._resolution_phase(player_skill, opponent_skill)

            if self._check_battle_end():
                self._show_text(self.player, "Returning to main menu...")
                self._transition_to_scene("MainMenuScene")
                break

    def _player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _opponent_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self._execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self._execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self._execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
            if self.player_creature.hp > 0:
                self._execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
        else:
            # Random decision when speeds are equal
            first, second = random.choice([(self.player, self.player_creature, player_skill),
                                           (self.opponent, self.opponent_creature, opponent_skill)])
            self._execute_skill(first[0], first[1], first[2], second[1])
            if second[1].hp > 0:
                self._execute_skill(second[0], second[1], second[2], first[1])

    def _execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        final_damage = max(0, raw_damage)  # Ensure damage is not negative
        defender_creature.hp = max(0, defender_creature.hp - final_damage)

        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"{defender_creature.display_name} took {final_damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
