from mini_game_engine.engine.lib import AbstractGameScene, Button
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
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} type)" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent Choice Phase
            opponent_skill = self._get_skill_choice(self.opponent, self.opponent_creature)

            # Resolution Phase
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            # Execute skills in order
            self._execute_skill(*first)
            if self._check_battle_end():
                self._show_text(self.player, "Returning to main menu...")
                self._transition_to_scene("MainMenuScene")
                return

            self._execute_skill(*second)
            if self._check_battle_end():
                self._show_text(self.player, "Returning to main menu...")
                self._transition_to_scene("MainMenuScene")
                return

    def _get_skill_choice(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _determine_order(self, action1, action2):
        if action1[1].speed > action2[1].speed:
            return action1, action2
        elif action2[1].speed > action1[1].speed:
            return action2, action1
        else:
            return random.sample([action1, action2], 2)

    def _get_type_multiplier(self, skill_type, creature_type):
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def _execute_skill(self, attacker, attacker_creature, skill):
        if attacker == self.player:
            defender = self.opponent
            defender_creature = self.opponent_creature
        else:
            defender = self.player
            defender_creature = self.player_creature

        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        type_multiplier = self._get_type_multiplier(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * type_multiplier)
        final_damage = max(1, final_damage)  # Minimum 1 damage

        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        effectiveness = "It's super effective!" if type_multiplier > 1 else "It's not very effective..." if type_multiplier < 1 else ""
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}! {effectiveness}")
        self._show_text(defender, f"{attacker_creature.display_name} used {skill.display_name}! {effectiveness}")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} was defeated!")
            self._show_text(self.opponent, f"Enemy {self.player_creature.display_name} was defeated!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"Enemy {self.opponent_creature.display_name} was defeated!")
            self._show_text(self.opponent, f"Your {self.opponent_creature.display_name} was defeated!")
            return True
        return False
