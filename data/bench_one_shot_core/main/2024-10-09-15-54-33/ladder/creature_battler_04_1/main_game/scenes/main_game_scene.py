from mini_game_engine.engine.lib import AbstractGameScene, Button
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Available skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while True:
            # Player turn
            player_skill = self._player_turn()
            
            # Opponent turn
            opponent_skill = self._opponent_turn()
            
            # Resolve turns
            self._resolve_turns(player_skill, opponent_skill)
            
            # Check for battle end
            if self._check_battle_end():
                break

    def _player_turn(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _opponent_turn(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return next(skill for skill in self.opponent_creature.skills if skill.display_name == choice.display_name)

    def _resolve_turns(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self._execute_skill(self.player_creature, self.opponent_creature, player_skill)
            if self.opponent_creature.hp > 0:
                self._execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self._execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
            if self.player_creature.hp > 0:
                self._execute_skill(self.player_creature, self.opponent_creature, player_skill)
        else:
            first, second = random.choice([(self.player_creature, self.opponent_creature), (self.opponent_creature, self.player_creature)])
            first_skill = player_skill if first == self.player_creature else opponent_skill
            second_skill = opponent_skill if first == self.player_creature else player_skill
            
            self._execute_skill(first, second, first_skill)
            if second.hp > 0:
                self._execute_skill(second, first, second_skill)

    def _execute_skill(self, attacker, defender, skill):
        damage = self._calculate_damage(attacker, defender, skill)
        damage = max(0, damage)  # Ensure no negative damage (no healing)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! {defender.display_name} took {damage} damage!")

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        return final_damage

    def _get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "normal": {"normal": 1, "fire": 1, "water": 1, "leaf": 1},
            "fire": {"normal": 1, "fire": 1, "water": 0.5, "leaf": 2},
            "water": {"normal": 1, "fire": 2, "water": 1, "leaf": 0.5},
            "leaf": {"normal": 1, "fire": 0.5, "water": 2, "leaf": 1}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self.player.reset_creatures()
            self.opponent.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self.player.reset_creatures()
            self.opponent.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False
