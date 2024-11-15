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
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
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
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")

    def _get_skill_choice(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _resolve_turn(self):
        first, second = self._determine_order()
        self._execute_skill(first)
        if second[1].hp > 0:  # Only execute second skill if target still alive
            self._execute_skill(second)

    def _determine_order(self):
        player_tuple = (self.player, self.player_creature, self.player_chosen_skill, self.opponent_creature)
        opponent_tuple = (self.opponent, self.opponent_creature, self.opponent_chosen_skill, self.player_creature)
        
        if self.player_creature.speed > self.opponent_creature.speed:
            return player_tuple, opponent_tuple
        elif self.player_creature.speed < self.opponent_creature.speed:
            return opponent_tuple, player_tuple
        else:
            return random.choice([(player_tuple, opponent_tuple), (opponent_tuple, player_tuple)])

    def _execute_skill(self, action_tuple):
        attacker_player, attacker, skill, defender = action_tuple
        damage = attacker.attack + skill.base_damage - defender.defense
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")
        self._show_text(self.opponent, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")
