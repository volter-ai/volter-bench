from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

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
        while True:
            player_skill = self._player_turn()
            opponent_skill = self._opponent_turn()

            first, second = self._determine_order(self.player_creature, self.opponent_creature, player_skill, opponent_skill)

            self._resolve_skill(*first)
            if self._check_battle_end():
                break

            self._resolve_skill(*second)
            if self._check_battle_end():
                break

    def _player_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _opponent_turn(self):
        return random.choice(self.opponent_creature.skills)

    def _determine_order(self, player_creature, opponent_creature, player_skill, opponent_skill):
        if player_creature.speed > opponent_creature.speed:
            return (self.player, player_creature, opponent_creature, player_skill), (self.opponent, opponent_creature, player_creature, opponent_skill)
        elif player_creature.speed < opponent_creature.speed:
            return (self.opponent, opponent_creature, player_creature, opponent_skill), (self.player, player_creature, opponent_creature, player_skill)
        else:
            if random.random() < 0.5:
                return (self.player, player_creature, opponent_creature, player_skill), (self.opponent, opponent_creature, player_creature, opponent_skill)
            else:
                return (self.opponent, opponent_creature, player_creature, opponent_skill), (self.player, player_creature, opponent_creature, player_skill)

    def _resolve_skill(self, attacker, attacker_creature, defender_creature, skill):
        damage = self._calculate_damage(attacker_creature, defender_creature, skill)
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"{defender_creature.display_name} took {damage} damage!")

    def _calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def _get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def _reset_creatures_state(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def _check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"{self.player.display_name}, you lost the battle!")
            self._reset_creatures_state()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"Congratulations {self.player.display_name}, you won the battle!")
            self._reset_creatures_state()
            self._transition_to_scene("MainMenuScene")
            return True
        return False
