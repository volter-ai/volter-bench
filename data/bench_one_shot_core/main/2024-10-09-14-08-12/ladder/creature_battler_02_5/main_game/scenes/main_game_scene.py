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
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        while True:
            battle_result = self._run_battle()
            if battle_result == "player_win":
                self._show_text(self.player, "You won the battle!")
            else:
                self._show_text(self.player, "You lost the battle!")

            play_again_button = Button("Play Again")
            quit_button = Button("Quit")
            choices = [play_again_button, quit_button]
            choice = self._wait_for_choice(self.player, choices)

            if choice == play_again_button:
                self._reset_battle()
            elif choice == quit_button:
                self._quit_whole_game()

    def _run_battle(self):
        while True:
            player_skill = self._player_choice_phase()
            opponent_skill = self._foe_choice_phase()
            self._resolution_phase(player_skill, opponent_skill)

            if self.player_creature.hp <= 0:
                return "opponent_win"
            elif self.opponent_creature.hp <= 0:
                return "player_win"

    def _reset_battle(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def _player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _foe_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def _resolution_phase(self, player_skill, opponent_skill):
        first, second = self._determine_order()
        self._execute_skill(first, second, player_skill if first == self.player else opponent_skill)
        if self.player_creature.hp > 0 and self.opponent_creature.hp > 0:
            self._execute_skill(second, first, opponent_skill if first == self.player else player_skill)

    def _determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return self.player, self.opponent
        elif self.player_creature.speed < self.opponent_creature.speed:
            return self.opponent, self.player
        else:
            return random.sample([self.player, self.opponent], 2)

    def _execute_skill(self, attacker, defender, skill):
        attacker_creature = attacker.creatures[0]
        defender_creature = defender.creatures[0]
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(0, damage)  # Ensure damage is not negative
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender_creature.display_name} took {damage} damage!")
