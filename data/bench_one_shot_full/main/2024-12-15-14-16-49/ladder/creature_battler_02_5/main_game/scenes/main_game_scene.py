from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.queued_actions = {}

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Attack: {self.player_creature.attack}
Defense: {self.player_creature.defense}
Speed: {self.player_creature.speed}

VS

{self.opponent.display_name}'s {self.opponent_creature.display_name}
HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp}
Attack: {self.opponent_creature.attack}
Defense: {self.opponent_creature.defense}
Speed: {self.opponent_creature.speed}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            self.queued_actions[self.player.uid] = player_skill

            # Opponent Choice Phase
            opponent_skill = self._get_skill_choice(self.opponent, self.opponent_creature)
            self.queued_actions[self.opponent.uid] = opponent_skill

            # Resolution Phase
            self._resolve_turn()

            # Check for battle end
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")

    def _get_skill_choice(self, player, creature):
        choices = [DictionaryChoice(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return creature.skills[choices.index(choice)]

    def _resolve_turn(self):
        first = self.player
        second = self.opponent

        # Determine order based on speed
        if self.opponent_creature.speed > self.player_creature.speed:
            first, second = second, first
        elif self.opponent_creature.speed == self.player_creature.speed:
            if random.random() < 0.5:
                first, second = second, first

        # Execute skills in order
        self._execute_skill(first, second)
        if second == self.player and self.player_creature.hp > 0 or \
           second == self.opponent and self.opponent_creature.hp > 0:
            self._execute_skill(second, first)

    def _execute_skill(self, attacker, defender):
        skill = self.queued_actions[attacker.uid]
        attacker_creature = self.player_creature if attacker == self.player else self.opponent_creature
        defender_creature = self.player_creature if defender == self.player else self.opponent_creature

        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        defender_creature.hp -= max(0, damage)

        self._show_text(self.player, 
            f"{attacker_creature.display_name} used {skill.display_name}! "
            f"Dealt {damage} damage to {defender_creature.display_name}!")
