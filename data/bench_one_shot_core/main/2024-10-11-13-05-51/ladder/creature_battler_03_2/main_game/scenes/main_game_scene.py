from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
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

Your skills:
{self._format_skills(self.player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        self._show_text(self.player, "A wild opponent appears!")
        self.battle_loop()

    def battle_loop(self):
        while True:
            player_skill = self._player_turn()
            opponent_skill = self._opponent_turn()

            first, second = self._determine_turn_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            self._resolve_turn(*first)
            if self._check_battle_end():
                self._end_battle()
                return

            self._resolve_turn(*second)
            if self._check_battle_end():
                self._end_battle()
                return

    def _player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _opponent_turn(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _determine_turn_order(self, player_data, opponent_data):
        if player_data[1].speed > opponent_data[1].speed:
            return player_data, opponent_data
        elif player_data[1].speed < opponent_data[1].speed:
            return opponent_data, player_data
        else:
            return random.sample([player_data, opponent_data], 2)

    def _resolve_turn(self, attacker, attacker_creature, skill):
        if attacker == self.player:
            defender = self.opponent
            defender_creature = self.opponent_creature
        else:
            defender = self.player
            defender_creature = self.player_creature

        damage = self._calculate_damage(attacker_creature, defender_creature, skill)
        defender_creature.hp = max(0, defender_creature.hp - damage)

        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} uses {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} takes {damage} damage!")

    def _calculate_damage(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        type_factor = self._get_type_factor(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_factor)

    def _get_type_factor(self, skill_type, creature_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)

    def _check_battle_end(self):
        return self.player_creature.hp == 0 or self.opponent_creature.hp == 0

    def _end_battle(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"{self.player.display_name}, you have lost the battle!")
        else:
            self._show_text(self.player, f"Congratulations {self.player.display_name}, you have won the battle!")
        
        self._show_text(self.player, "Returning to the main menu...")
        self._transition_to_scene("MainMenuScene")
