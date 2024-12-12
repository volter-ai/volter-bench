from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_chosen_skill = None
        self.opponent_chosen_skill = None

    def __str__(self):
        return f"""=== Battle Scene ===
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
            self.player_chosen_skill = self._wait_for_choice(
                self.player,
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Opponent Choice Phase
            self.opponent_chosen_skill = self._wait_for_choice(
                self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]
            ).thing

            # Resolution Phase
            first, second = self.determine_order()
            
            # Execute first attack
            damage = self.calculate_damage(first[0], first[1], first[2], first[3])
            first[3].hp -= damage
            self._show_text(self.player, f"{first[1].display_name} used {first[2].display_name} for {damage} damage!")
            self._show_text(self.opponent, f"{first[1].display_name} used {first[2].display_name} for {damage} damage!")
            
            if self.check_battle_end():
                return

            # Execute second attack
            damage = self.calculate_damage(second[0], second[1], second[2], second[3])
            second[3].hp -= damage
            self._show_text(self.player, f"{second[1].display_name} used {second[2].display_name} for {damage} damage!")
            self._show_text(self.opponent, f"{second[1].display_name} used {second[2].display_name} for {damage} damage!")
            
            if self.check_battle_end():
                return

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.player_creature, self.player_chosen_skill, self.opponent_creature), \
                   (self.opponent, self.opponent_creature, self.opponent_chosen_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.opponent_creature, self.opponent_chosen_skill, self.player_creature), \
                   (self.player, self.player_creature, self.player_chosen_skill, self.opponent_creature)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_creature, self.player_chosen_skill, self.opponent_creature), \
                       (self.opponent, self.opponent_creature, self.opponent_chosen_skill, self.player_creature)
            else:
                return (self.opponent, self.opponent_creature, self.opponent_chosen_skill, self.player_creature), \
                       (self.player, self.player_creature, self.player_chosen_skill, self.opponent_creature)

    def calculate_damage(self, attacker, attacker_creature, skill, defender_creature):
        return max(0, attacker_creature.attack + skill.base_damage - defender_creature.defense)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._show_text(self.opponent, "You won!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._show_text(self.opponent, "You lost!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
