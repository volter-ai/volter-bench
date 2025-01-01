import random
from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

    def __str__(self):
        return f"""=== Battle Scene ===
Player: {self.player.display_name}
Opponent: {self.opponent.display_name}

Player's Creatures:
{self._creature_status(self.player.creatures)}

Opponent's Creatures:
{self._creature_status(self.opponent.creatures)}
"""

    def _creature_status(self, creatures):
        return "\n".join([f"{c.display_name}: {c.hp}/{c.max_hp} HP" for c in creatures])

    def run(self):
        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()
            if self.check_battle_end():
                break

    def player_choice_phase(self):
        player_creature = self.player.creatures[0]
        choices = [SelectThing(skill) for skill in player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_action = choice.thing

    def foe_choice_phase(self):
        opponent_creature = self.opponent.creatures[0]
        self.opponent_action = random.choice(opponent_creature.skills)

    def resolution_phase(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        actions = [(player_creature, self.player_action), (opponent_creature, self.opponent_action)]
        actions.sort(key=lambda x: x[0].speed, reverse=True)

        # Check if both creatures have the same speed
        if player_creature.speed == opponent_creature.speed:
            random.shuffle(actions)  # Randomly shuffle the order if speeds are equal

        for creature, action in actions:
            if creature.hp > 0:
                target = opponent_creature if creature == player_creature else player_creature
                damage = max(0, creature.attack + action.base_damage - target.defense)
                target.hp = max(0, target.hp - damage)
                self._show_text(self.player, f"{creature.display_name} used {action.display_name} dealing {damage} damage!")

    def check_battle_end(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        if player_creature.hp == 0 or opponent_creature.hp == 0:
            winner = "Player" if opponent_creature.hp == 0 else "Opponent"
            self._show_text(self.player, f"{winner} wins the battle!")
            self._quit_whole_game()  # Properly end the game
            return True
        return False
