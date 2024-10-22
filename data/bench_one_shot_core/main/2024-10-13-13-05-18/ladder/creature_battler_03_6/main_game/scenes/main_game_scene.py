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

Available skills:
{self._format_skills(self.player_creature.skills)}

> Return to Main Menu
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def run(self):
        while True:
            # Player Choice Phase
            player_choice = self._player_choice_phase()
            
            if isinstance(player_choice, Button) and player_choice.display_name == "Return to Main Menu":
                self._transition_to_scene("MainMenuScene")
                return

            # Foe Choice Phase
            foe_skill = self._foe_choice_phase()

            # Resolution Phase
            self._resolution_phase(player_choice, foe_skill)

            # Check for battle end
            if self._check_battle_end():
                self._transition_to_scene("MainMenuScene")
                return

    def _player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choices.append(Button("Return to Main Menu"))
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing if isinstance(choice, SelectThing) else choice

    def _foe_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def _resolution_phase(self, player_skill, foe_skill):
        first, second = self._determine_order(self.player_creature, self.opponent_creature)
        first_skill = player_skill if first == self.player_creature else foe_skill
        second_skill = foe_skill if first == self.player_creature else player_skill

        self._execute_skill(first, second, first_skill)
        if second.hp > 0:
            self._execute_skill(second, first, second_skill)

    def _determine_order(self, creature1, creature2):
        if creature1.speed > creature2.speed:
            return creature1, creature2
        elif creature2.speed > creature1.speed:
            return creature2, creature1
        else:
            return random.sample([creature1, creature2], 2)

    def _execute_skill(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        factor = self._get_weakness_resistance_factor(skill.skill_type, defender.creature_type)
        final_damage = int(factor * raw_damage)
        defender.hp = max(0, defender.hp - final_damage)

        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")

    def _get_weakness_resistance_factor(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1
        elif skill_type == "fire" and creature_type == "leaf":
            return 2
        elif skill_type == "fire" and creature_type == "water":
            return 0.5
        elif skill_type == "water" and creature_type == "fire":
            return 2
        elif skill_type == "water" and creature_type == "leaf":
            return 0.5
        elif skill_type == "leaf" and creature_type == "water":
            return 2
        elif skill_type == "leaf" and creature_type == "fire":
            return 0.5
        else:
            return 1

    def _check_battle_end(self):
        if self.player_creature.hp == 0:
            self._show_text(self.player, f"{self.player.display_name}, you have lost the battle!")
            return True
        elif self.opponent_creature.hp == 0:
            self._show_text(self.player, f"Congratulations {self.player.display_name}, you have won the battle!")
            return True
        return False
