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
            
            # Check for battle end
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._show_text(self.opponent, "You won!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._show_text(self.opponent, "You lost!")
                break

        self._transition_to_scene("MainMenuScene")

    def _get_skill_choice(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return creature.skills[choices.index(choice)]

    def _resolve_turn(self):
        first, second = self._determine_turn_order()
        
        self._execute_skill(first[0], first[1], first[2], first[3])
        if second[1].hp > 0:  # Only execute second skill if target still alive
            self._execute_skill(second[0], second[1], second[2], second[3])

    def _determine_turn_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.opponent_creature, self.player_creature, self.player_chosen_skill), \
                   (self.opponent, self.player_creature, self.opponent_creature, self.opponent_chosen_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.player_creature, self.opponent_creature, self.opponent_chosen_skill), \
                   (self.player, self.opponent_creature, self.player_creature, self.player_chosen_skill)
        else:
            if random.random() < 0.5:
                return (self.player, self.opponent_creature, self.player_creature, self.player_chosen_skill), \
                       (self.opponent, self.player_creature, self.opponent_creature, self.opponent_chosen_skill)
            else:
                return (self.opponent, self.player_creature, self.opponent_creature, self.opponent_chosen_skill), \
                       (self.player, self.opponent_creature, self.player_creature, self.player_chosen_skill)

    def _execute_skill(self, user, target, attacker, skill):
        damage = attacker.attack + skill.base_damage - target.defense
        target.hp -= max(0, damage)
        self._show_text(user, f"{attacker.display_name} used {skill.display_name}!")
