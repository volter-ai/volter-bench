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
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
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
            first, second = self._determine_turn_order()
            
            # Execute skills
            self._execute_skill(first[0], first[1], first[2], first[3])
            if self._check_battle_end():
                break
                
            self._execute_skill(second[0], second[1], second[2], second[3])
            if self._check_battle_end():
                break

    def _get_skill_choice(self, actor, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(actor, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _determine_turn_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            first = (self.player, self.player_creature, self.opponent_creature, self.player_chosen_skill)
            second = (self.opponent, self.opponent_creature, self.player_creature, self.opponent_chosen_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            first = (self.opponent, self.opponent_creature, self.player_creature, self.opponent_chosen_skill)
            second = (self.player, self.player_creature, self.opponent_creature, self.player_chosen_skill)
        else:
            if random.random() < 0.5:
                first = (self.player, self.player_creature, self.opponent_creature, self.player_chosen_skill)
                second = (self.opponent, self.opponent_creature, self.player_creature, self.opponent_chosen_skill)
            else:
                first = (self.opponent, self.opponent_creature, self.player_creature, self.opponent_chosen_skill)
                second = (self.player, self.player_creature, self.opponent_creature, self.player_chosen_skill)
        return first, second

    def _execute_skill(self, actor, attacker, defender, skill):
        damage = attacker.attack + skill.base_damage - defender.defense
        defender.hp -= damage
        self._show_text(actor, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(actor, f"Dealt {damage} damage!")

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
