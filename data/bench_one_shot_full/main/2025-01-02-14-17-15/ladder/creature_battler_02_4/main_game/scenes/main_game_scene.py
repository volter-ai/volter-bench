from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        return f"""=== Main Game Scene ===
Player: {self.player.display_name}
Opponent: {self.opponent.display_name}
"""

    def run(self):
        while True:
            player_creature = self.player.creatures[0]
            opponent_creature = self.opponent.creatures[0]

            # Player Choice Phase
            player_choice = self._wait_for_choice(self.player, [
                SelectThing(skill) for skill in player_creature.skills
            ])

            # Foe Choice Phase
            opponent_choice = self._wait_for_choice(self.opponent, [
                SelectThing(skill) for skill in opponent_creature.skills
            ])

            # Resolution Phase
            self.resolve_turn(player_creature, opponent_creature, player_choice, opponent_choice)

            # Check for end condition
            if player_creature.hp <= 0 or opponent_creature.hp <= 0:
                self.end_battle(player_creature, opponent_creature)
                break

    def resolve_turn(self, player_creature: Creature, opponent_creature: Creature, player_choice, opponent_choice):
        # Determine order based on speed
        if player_creature.speed > opponent_creature.speed:
            self.execute_skill(player_creature, opponent_creature, player_choice)
            if opponent_creature.hp > 0:
                self.execute_skill(opponent_creature, player_creature, opponent_choice)
        else:
            self.execute_skill(opponent_creature, player_creature, opponent_choice)
            if player_creature.hp > 0:
                self.execute_skill(player_creature, opponent_creature, player_choice)

    def execute_skill(self, attacker: Creature, defender: Creature, skill_choice):
        skill = skill_choice.thing
        damage = max(0, attacker.attack + skill.base_damage - defender.defense)
        defender.hp -= damage
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} dealing {damage} damage!")

    def end_battle(self, player_creature: Creature, opponent_creature: Creature):
        if player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")
        self._quit_whole_game()
