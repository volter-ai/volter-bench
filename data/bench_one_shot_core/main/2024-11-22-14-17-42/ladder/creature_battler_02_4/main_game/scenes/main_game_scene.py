from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_chosen_skill = None
        self.opponent_chosen_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Your turn!")
            self.player_chosen_skill = self._get_skill_choice(self.player, self.player_creature)

            # Opponent choice phase
            self._show_text(self.opponent, "Your turn!")
            self.opponent_chosen_skill = self._get_skill_choice(self.opponent, self.opponent_creature)

            # Resolution phase
            self._resolve_turn()

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._show_text(self.opponent, "You won!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._show_text(self.opponent, "You lost!")
                break

        self._transition_to_scene("MainMenuScene")

    def _get_skill_choice(self, actor, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(actor, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolve_turn(self):
        # Determine order based on speed
        if self.player_creature.speed > self.opponent_creature.speed:
            first, second = self.player, self.opponent
            first_skill, second_skill = self.player_chosen_skill, self.opponent_chosen_skill
        elif self.opponent_creature.speed > self.player_creature.speed:
            first, second = self.opponent, self.player
            first_skill, second_skill = self.opponent_chosen_skill, self.player_chosen_skill
        else:
            if random.random() < 0.5:
                first, second = self.player, self.opponent
                first_skill, second_skill = self.player_chosen_skill, self.opponent_chosen_skill
            else:
                first, second = self.opponent, self.player
                first_skill, second_skill = self.opponent_chosen_skill, self.player_chosen_skill

        # Execute skills in order
        self._execute_skill(first, first_skill)
        if (first == self.player and self.opponent_creature.hp > 0) or \
           (first == self.opponent and self.player_creature.hp > 0):
            self._execute_skill(second, second_skill)

    def _execute_skill(self, actor, skill):
        if actor == self.player:
            attacker = self.player_creature
            defender = self.opponent_creature
        else:
            attacker = self.opponent_creature
            defender = self.player_creature

        damage = attacker.attack + skill.base_damage - defender.defense
        defender.hp = max(0, defender.hp - damage)

        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")
        self._show_text(self.opponent, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")
