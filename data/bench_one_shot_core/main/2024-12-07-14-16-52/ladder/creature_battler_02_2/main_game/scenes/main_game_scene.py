from mini_game_engine.engine.lib import AbstractGameScene, Button
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

VS

{self.opponent.display_name}'s {self.opponent_creature.display_name}
HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp}
Attack: {self.opponent_creature.attack}
Defense: {self.opponent_creature.defense}
Speed: {self.opponent_creature.speed}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        while True:
            # Player Choice Phase
            self._show_text(self.player, "Choose your skill!")
            self.player_chosen_skill = self._wait_for_choice(
                self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills]
            )

            # Opponent Choice Phase
            self._show_text(self.opponent, "Choose your skill!")
            self.opponent_chosen_skill = self._wait_for_choice(
                self.opponent,
                [Button(skill.display_name) for skill in self.opponent_creature.skills]
            )

            # Resolution Phase
            first, second = self.determine_order()
            
            # Execute first attack
            damage = self.calculate_damage(first[0], first[1])
            first[1].hp -= damage
            self._show_text(self.player, f"{first[0].display_name} deals {damage} damage to {first[1].display_name}!")
            
            if self.check_battle_end():
                return

            # Execute second attack
            damage = self.calculate_damage(second[0], second[1])
            second[1].hp -= damage
            self._show_text(self.player, f"{second[0].display_name} deals {damage} damage to {second[1].display_name}!")
            
            if self.check_battle_end():
                return

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player_creature, self.opponent_creature), (self.opponent_creature, self.player_creature)
        elif self.opponent_creature.speed > self.player_creature.speed:
            return (self.opponent_creature, self.player_creature), (self.player_creature, self.opponent_creature)
        else:
            if random.random() < 0.5:
                return (self.player_creature, self.opponent_creature), (self.opponent_creature, self.player_creature)
            return (self.opponent_creature, self.player_creature), (self.player_creature, self.opponent_creature)

    def calculate_damage(self, attacker, defender):
        skill = attacker.skills[0]  # For now just use tackle
        return attacker.attack + skill.base_damage - defender.defense

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
