from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
        return "\n".join([f"> {skill.display_name} ({skill.skill_type} type, {skill.base_damage} damage)" for skill in skills])

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
        while True:
            battle_result = self._battle_round()
            if battle_result:
                self._end_battle(battle_result)
                break

    def _battle_round(self):
        player_skill = self._player_choice_phase()
        opponent_skill = self._foe_choice_phase()
        return self._resolution_phase(player_skill, opponent_skill)

    def _player_choice_phase(self):
        choices = [SelectThing(skill, label=f"{skill.display_name} ({skill.skill_type} type, {skill.base_damage} damage)") for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def _foe_choice_phase(self):
        choices = [SelectThing(skill, label=f"{skill.display_name} ({skill.skill_type} type, {skill.base_damage} damage)") for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _resolution_phase(self, player_skill, opponent_skill):
        first, second = self._determine_order(self.player_creature, self.opponent_creature, player_skill, opponent_skill)
        for attacker, defender, skill in [first, second]:
            damage = self._calculate_damage(attacker, defender, skill)
            defender.hp = max(0, defender.hp - damage)
            self._show_text(self.player, f"{attacker.display_name} uses {skill.display_name} and deals {damage} damage to {defender.display_name}!")
            if defender.hp == 0:
                winner = self.player if defender == self.opponent_creature else self.opponent
                self._show_text(self.player, f"{defender.display_name} fainted! {winner.display_name} wins!")
                return winner
        return None

    def _determine_order(self, creature1, creature2, skill1, skill2):
        if creature1.speed > creature2.speed or (creature1.speed == creature2.speed and random.choice([True, False])):
            return (creature1, creature2, skill1), (creature2, creature1, skill2)
        else:
            return (creature2, creature1, skill2), (creature1, creature2, skill1)

    def _calculate_damage(self, attacker, defender, skill):
        raw_damage = float(attacker.attack) + float(skill.base_damage) - float(defender.defense)
        effectiveness = self._get_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = raw_damage * effectiveness
        return max(1, int(final_damage))  # Convert to int at the end and ensure at least 1 damage

    def _get_effectiveness(self, skill_type, defender_type):
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def _end_battle(self, winner):
        self._show_text(self.player, f"Battle ended! {winner.display_name} is victorious!")
        choices = [
            Button("Play Again"),
            Button("Quit")
        ]
        choice = self._wait_for_choice(self.player, choices)
        if choice.display_name == "Play Again":
            self._transition_to_scene("MainMenuScene")
        else:
            self._quit_whole_game()
