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
Your Creature: {player_creature.display_name} (HP: {player_creature.hp}/{player_creature.max_hp})
Opponent's Creature: {opponent_creature.display_name} (HP: {opponent_creature.hp}/{opponent_creature.max_hp})
Choose a skill:
"""

    def run(self):
        while self.player.creatures[0].hp > 0 and self.opponent.creatures[0].hp > 0:
            self.player_turn()
            if self.opponent.creatures[0].hp <= 0:
                self._show_text(self.player, "You win!")
                break
            self.opponent_turn()
            if self.player.creatures[0].hp <= 0:
                self._show_text(self.player, "You lose!")
                break

        # Reset the state of the player's creatures
        self.reset_creatures_state()

        # Transition back to the MainMenuScene after the battle ends
        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        player_creature = self.player.creatures[0]
        choices = [SelectThing(skill) for skill in player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.resolve_skill(player_creature, self.opponent.creatures[0], choice.thing)

    def opponent_turn(self):
        opponent_creature = self.opponent.creatures[0]
        choice = self.opponent._listener.on_wait_for_choice(self, [SelectThing(skill) for skill in opponent_creature.skills])
        self.resolve_skill(opponent_creature, self.player.creatures[0], choice.thing)

    def resolve_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        defender.hp -= skill.damage
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! {defender.display_name} took {skill.damage} damage.")

    def reset_creatures_state(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
