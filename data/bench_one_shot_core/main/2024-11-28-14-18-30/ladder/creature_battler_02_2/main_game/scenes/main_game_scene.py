from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        
    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.opponent, "Battle Start!")

        while True:
            # Player Choice Phase
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing

            # Opponent Choice Phase  
            opponent_skill = self._wait_for_choice(self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]).thing

            # Resolution Phase
            first, second = self.determine_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            # Execute moves in order
            damage = self.execute_skill(first[1], first[2], second[1])
            self._show_text(first[0], f"{first[1].display_name} used {first[2].display_name}!")
            self._show_text(second[0], f"Took {damage} damage!")

            if second[1].hp <= 0:
                self._show_text(self.player, f"{second[1].display_name} fainted! {first[0].display_name} wins!")
                self._transition_to_scene("MainMenuScene")
                return

            damage = self.execute_skill(second[1], second[2], first[1])
            self._show_text(second[0], f"{second[1].display_name} used {second[2].display_name}!")
            self._show_text(first[0], f"Took {damage} damage!")

            if first[1].hp <= 0:
                self._show_text(self.player, f"{first[1].display_name} fainted! {second[0].display_name} wins!")
                self._transition_to_scene("MainMenuScene")
                return

    def determine_order(self, a, b):
        if a[1].speed > b[1].speed:
            return a, b
        elif b[1].speed > a[1].speed:
            return b, a
        else:
            return random.choice([(a, b), (b, a)])

    def execute_skill(self, attacker, skill, defender):
        damage = max(0, attacker.attack + skill.base_damage - defender.defense)
        defender.hp -= damage
        return damage
