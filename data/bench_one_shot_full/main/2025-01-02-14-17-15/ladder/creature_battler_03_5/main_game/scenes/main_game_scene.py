from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot(prototype_id="basic_opponent")

    def __str__(self):
        return (
            f"=== Battle ===\n"
            f"Player: {self.player.display_name} - Creature: {self.player.creatures[0].display_name}\n"
            f"Opponent: {self.opponent.display_name} - Creature: {self.opponent.creatures[0].display_name}\n"
        )

    def run(self):
        while True:
            player_choice = self._wait_for_choice(
                self.player, [SelectThing(skill) for skill in self.player.creatures[0].skills]
            )
            opponent_choice = self._wait_for_choice(
                self.opponent, [SelectThing(skill) for skill in self.opponent.creatures[0].skills]
            )
            self.resolve_turn(player_choice, opponent_choice)

    def resolve_turn(self, player_choice, opponent_choice):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        # Determine turn order based on speed
        if player_creature.speed > opponent_creature.speed:
            self.execute_skill(player_creature, opponent_creature, player_choice.thing)
            if opponent_creature.hp > 0:
                self.execute_skill(opponent_creature, player_creature, opponent_choice.thing)
        else:
            self.execute_skill(opponent_creature, player_creature, opponent_choice.thing)
            if player_creature.hp > 0:
                self.execute_skill(player_creature, opponent_creature, player_choice.thing)

        # Check for battle end condition
        if player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._quit_whole_game()
        elif opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._quit_whole_game()

    def execute_skill(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        final_damage = self.calculate_final_damage(skill.skill_type, defender.creature_type, raw_damage)
        defender.hp = max(0, defender.hp - int(final_damage))

    def calculate_final_damage(self, skill_type, defender_type, raw_damage):
        type_effectiveness = {
            "normal": {},
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        factor = type_effectiveness.get(skill_type, {}).get(defender_type, 1)
        return raw_damage * factor
