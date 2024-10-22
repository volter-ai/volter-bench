import random

from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        while not self.battle_ended:
            player_skill = self._player_turn()
            opponent_skill = self._opponent_turn()
            self._resolve_turn(player_skill, opponent_skill)
            self.battle_ended = self._check_battle_end()
        
        self._end_battle()

    def _player_turn(self):
        self._show_text(self.player, "Your turn!")
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _opponent_turn(self):
        self._show_text(self.opponent, "Opponent's turn!")
        return random.choice(self.opponent_creature.skills)

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
            # Equal speed, random order
            if random.choice([True, False]):
                self._execute_skill(self.player_creature, player_skill, self.opponent_creature)
                if self.opponent_creature.hp > 0:
                    self._execute_skill(self.opponent_creature, opponent_skill, self.player_creature)
            else:
                self._execute_skill(self.opponent_creature, opponent_skill, self.player_creature)
                if self.player_creature.hp > 0:
                    self._execute_skill(self.player_creature, player_skill, self.opponent_creature)

    def _execute_skill(self, attacker, skill, defender):
        damage = self._calculate_damage(attacker, skill, defender)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! {defender.display_name} took {damage} damage!")

    def _calculate_damage(self, attacker, skill, defender):
        if skill.is_physical:
            raw_damage = float(attacker.attack) + float(skill.base_damage) - float(defender.defense)
        else:
            raw_damage = (float(attacker.sp_attack) / float(defender.sp_defense)) * float(skill.base_damage)
        
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)  # Convert to integer here
        return final_damage

    def _get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _end_battle(self):
        self._reset_player_creatures()
        self._show_text(self.player, "Returning to main menu...")
        self._transition_to_scene("MainMenuScene")

    def _reset_player_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
