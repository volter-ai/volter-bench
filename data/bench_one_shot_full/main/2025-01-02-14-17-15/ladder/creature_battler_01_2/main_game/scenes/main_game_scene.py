from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("default_player")

    def __str__(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]
        return f"""=== Battle ===
Player: {self.player.display_name}
Creature: {player_creature.display_name} (HP: {player_creature.hp}/{player_creature.max_hp})

Opponent: {self.opponent.display_name}
Creature: {opponent_creature.display_name} (HP: {opponent_creature.hp}/{opponent_creature.max_hp})

Choose your action:
"""

    def run(self):
        while True:
            player_creature = self.player.creatures[0]
            opponent_creature = self.opponent.creatures[0]

            if player_creature.hp <= 0 or opponent_creature.hp <= 0:
                self._show_text(self.player, "Battle Over!")
                self.handle_battle_end(player_creature, opponent_creature)
                break

            player_choice = self._wait_for_choice(self.player, [SelectThing(skill) for skill in player_creature.skills])
            opponent_choice = self._wait_for_choice(self.opponent, [SelectThing(skill) for skill in opponent_creature.skills])

            self.resolve_turn(player_choice.thing, opponent_choice.thing, player_creature, opponent_creature)

    def resolve_turn(self, player_skill: Skill, opponent_skill: Skill, player_creature: Creature, opponent_creature: Creature):
        opponent_creature.hp -= player_skill.damage
        player_creature.hp -= opponent_skill.damage
        self._show_text(self.player, f"You used {player_skill.display_name}, dealing {player_skill.damage} damage!")
        self._show_text(self.opponent, f"Opponent used {opponent_skill.display_name}, dealing {opponent_skill.damage} damage!")

    def handle_battle_end(self, player_creature: Creature, opponent_creature: Creature):
        if player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
        elif opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")

        # Transition back to the main menu or quit the game
        self._transition_to_scene("MainMenuScene")
