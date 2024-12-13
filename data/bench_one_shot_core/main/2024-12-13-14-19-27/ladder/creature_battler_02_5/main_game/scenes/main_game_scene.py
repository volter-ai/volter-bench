from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
            self.player_chosen_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent Choice Phase
            self.opponent_chosen_skill = self._get_skill_choice(self.opponent, self.opponent_creature)

            # Resolution Phase
            self._resolve_turn()

            if self._check_battle_end():
                break

    def _get_skill_choice(self, acting_player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        return self._wait_for_choice(acting_player, choices).thing

    def _resolve_turn(self):
        first, second = self._determine_turn_order()
        
        # First attack
        damage = self._calculate_damage(first[0], first[1], first[2], first[3])
        first[3].hp -= damage
        self._show_text(self.player, f"{first[0].display_name}'s {first[1].display_name} used {first[2].display_name} for {damage} damage!")
        self._show_text(self.opponent, f"{first[0].display_name}'s {first[1].display_name} used {first[2].display_name} for {damage} damage!")

        if not self._check_battle_end():
            # Second attack
            damage = self._calculate_damage(second[0], second[1], second[2], second[3])
            second[3].hp -= damage
            self._show_text(self.player, f"{second[0].display_name}'s {second[1].display_name} used {second[2].display_name} for {damage} damage!")
            self._show_text(self.opponent, f"{second[0].display_name}'s {second[1].display_name} used {second[2].display_name} for {damage} damage!")

    def _determine_turn_order(self):
        player_data = (self.player, self.player_creature, self.player_chosen_skill, self.opponent_creature)
        opponent_data = (self.opponent, self.opponent_creature, self.opponent_chosen_skill, self.player_creature)
        
        if self.player_creature.speed > self.opponent_creature.speed:
            return player_data, opponent_data
        elif self.player_creature.speed < self.opponent_creature.speed:
            return opponent_data, player_data
        else:
            return (player_data, opponent_data) if random.random() < 0.5 else (opponent_data, player_data)

    def _calculate_damage(self, attacker, attacker_creature, skill, defender_creature):
        return max(0, attacker_creature.attack + skill.base_damage - defender_creature.defense)

    def _check_battle_end(self):
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
