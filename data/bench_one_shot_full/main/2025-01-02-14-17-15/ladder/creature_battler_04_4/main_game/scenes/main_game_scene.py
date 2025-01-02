from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    TYPE_EFFECTIVENESS = {
        ("fire", "leaf"): 2.0,
        ("leaf", "water"): 2.0,
        ("water", "fire"): 2.0,
        ("leaf", "fire"): 0.5,
        ("water", "leaf"): 0.5,
        ("fire", "water"): 0.5,
    }

    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        return f"""=== Battle Scene ===
Player: {self.player.display_name}
Opponent: {self.opponent.display_name}

Player's Creature: {self.player.creatures[0].display_name} (HP: {self.player.creatures[0].hp})
Opponent's Creature: {self.opponent.creatures[0].display_name} (HP: {self.opponent.creatures[0].hp})
"""

    def run(self):
        while True:
            if self.player.creatures[0].hp <= 0:
                self._show_text(self.player, "You lose!")
                break
            elif self.opponent.creatures[0].hp <= 0:
                self._show_text(self.player, "You win!")
                break

            self.resolve_turn()

        self.reset_creature_states()
        self._transition_to_scene("MainMenuScene")

    def resolve_turn(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        player_choice = self._wait_for_choice(self.player, [SelectThing(skill) for skill in player_creature.skills])
        opponent_choice = self.opponent._listener.on_wait_for_choice(self, [SelectThing(s) for s in opponent_creature.skills])

        actions = [(player_creature, opponent_creature, player_choice.thing), 
                   (opponent_creature, player_creature, opponent_choice.thing)]

        # Sort actions by speed, randomize if speeds are equal
        actions.sort(key=lambda x: x[0].speed, reverse=True)
        if actions[0][0].speed == actions[1][0].speed:
            random.shuffle(actions)

        for attacker, defender, skill in actions:
            if defender.hp > 0:  # Only attack if the defender is still alive
                self.execute_skill(attacker, defender, skill)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_effectiveness = self.TYPE_EFFECTIVENESS.get((skill.skill_type, defender.creature_type), 1.0)
        final_damage = int(type_effectiveness * raw_damage)

        defender.hp = max(defender.hp - final_damage, 0)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} dealing {final_damage} damage!")

    def reset_creature_states(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
