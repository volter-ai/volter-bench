from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
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
{self.player.display_name}'s {self.player_creature.display_name}
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Attack: {self.player_creature.attack}
Defense: {self.player_creature.defense}
Speed: {self.player_creature.speed}

{self.opponent.display_name}'s {self.opponent_creature.display_name}
HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp}
Attack: {self.opponent_creature.attack}
Defense: {self.opponent_creature.defense}
Speed: {self.opponent_creature.speed}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.opponent, "Battle Start!")

        while True:
            # Player choice phase
            self.player_chosen_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent choice phase
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

    def _get_skill_choice(self, player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        return self._wait_for_choice(player, choices).thing

    def _resolve_turn(self):
        # Determine order
        first = self.player
        second = self.opponent
        first_creature = self.player_creature
        second_creature = self.opponent_creature
        first_skill = self.player_chosen_skill
        second_skill = self.opponent_chosen_skill

        if self.opponent_creature.speed > self.player_creature.speed or \
           (self.opponent_creature.speed == self.player_creature.speed and random.random() < 0.5):
            first, second = second, first
            first_creature, second_creature = second_creature, first_creature
            first_skill, second_skill = second_skill, first_skill

        # Execute skills
        self._execute_skill(first, first_creature, first_skill, second_creature)
        if second_creature.hp > 0:
            self._execute_skill(second, second_creature, second_skill, first_creature)

    def _execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(0, damage)  # Prevent negative damage
        defender_creature.hp -= damage
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name} for {damage} damage!")
        self._show_text(self.opponent, f"{attacker_creature.display_name} used {skill.display_name} for {damage} damage!")
