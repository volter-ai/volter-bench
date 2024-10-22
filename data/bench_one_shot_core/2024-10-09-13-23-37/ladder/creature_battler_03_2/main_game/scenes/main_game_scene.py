import random

from mini_game_engine.engine.lib import AbstractGameScene, Button


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your skills:
{self._get_skill_choices_str(self.player_creature)}

Opponent's skills:
{self._get_skill_choices_str(self.opponent_creature)}

Your turn! Choose a skill:
"""

    def _get_skill_choices_str(self, creature):
        return "\n".join([f"> {skill.display_name}" for skill in creature.skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        self.game_loop()

    def game_loop(self):
        while True:
            # Player turn
            player_skill = self._player_turn()
            
            # Opponent turn
            opponent_skill = self._opponent_turn()
            
            # Resolve turn
            self._resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            if self._check_battle_end():
                break

    def _player_turn(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _opponent_turn(self):
        opponent_skill = random.choice(self.opponent_creature.skills)
        self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} chose {opponent_skill.display_name}!")
        return opponent_skill

    def _resolve_turn(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self._execute_skill(self.player_creature, player_skill, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self._execute_skill(self.opponent_creature, opponent_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self._execute_skill(self.opponent_creature, opponent_skill, self.player_creature)
            if self.player_creature.hp > 0:
                self._execute_skill(self.player_creature, player_skill, self.opponent_creature)
        else:
            # Equal speeds, randomly decide who goes first
            if random.choice([True, False]):
                self._execute_skill(self.player_creature, player_skill, self.opponent_creature)
                if self.opponent_creature.hp > 0:
                    self._execute_skill(self.opponent_creature, opponent_skill, self.player_creature)
            else:
                self._execute_skill(self.opponent_creature, opponent_skill, self.player_creature)
                if self.player_creature.hp > 0:
                    self._execute_skill(self.player_creature, player_skill, self.opponent_creature)

    def _execute_skill(self, attacker, skill, defender):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        weakness_factor = self._get_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")

    def _get_weakness_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1  # Normal type is neither effective nor ineffective against any type
        elif skill_type == defender_type:
            return 1  # Same type is neither effective nor ineffective
        elif (skill_type == "fire" and defender_type == "water") or \
             (skill_type == "water" and defender_type == "fire"):
            return 0.5  # Ineffective: half damage
        elif (skill_type == "fire" and defender_type == "water") or \
             (skill_type == "water" and defender_type == "fire"):
            return 2  # Effective: double damage
        else:
            return 1  # Default case: normal damage

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} fainted! You lost the battle.")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"The opponent's {self.opponent_creature.display_name} fainted! You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
