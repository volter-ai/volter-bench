from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_action = None
        self.foe_action = None

    def __str__(self):
        return f"""===Main Game===
Player: {self.player.display_name}
Active Creature: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})

Opponent: {self.opponent.display_name}
Active Creature: {self.opponent.active_creature.display_name} (HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp})
"""

    def run(self):
        while self.player.creatures and self.opponent.creatures:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()
            self.check_knockouts()

    def player_choice_phase(self):
        choices = [Button("Attack"), Button("Swap")]
        choice = self._wait_for_choice(self.player, choices)

        if choice.display_name == "Attack":
            skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
            skill_choice = self._wait_for_choice(self.player, skill_choices)
            self.player_action = skill_choice.thing
        elif choice.display_name == "Swap":
            swap_choices = [SelectThing(creature) for creature in self.player.creatures if creature != self.player.active_creature and creature.hp > 0]
            swap_choice = self._wait_for_choice(self.player, swap_choices)
            self.player.active_creature = swap_choice.thing
            self.player_action = None  # No attack if swapped

    def foe_choice_phase(self):
        if random.choice([True, False]):
            self.foe_action = random.choice(self.opponent.active_creature.skills)
        else:
            self.opponent.active_creature = random.choice([creature for creature in self.opponent.creatures if creature != self.opponent.active_creature and creature.hp > 0])
            self.foe_action = None  # No attack if swapped

    def resolution_phase(self):
        if self.player_action and self.foe_action:
            # Determine order based on speed
            if self.player.active_creature.speed > self.opponent.active_creature.speed:
                self.execute_skill(self.player.active_creature, self.opponent.active_creature, self.player_action)
                if self.opponent.active_creature.hp > 0:
                    self.execute_skill(self.opponent.active_creature, self.player.active_creature, self.foe_action)
            else:
                self.execute_skill(self.opponent.active_creature, self.player.active_creature, self.foe_action)
                if self.player.active_creature.hp > 0:
                    self.execute_skill(self.player.active_creature, self.opponent.active_creature, self.player_action)
        elif self.player_action:
            self.execute_skill(self.player.active_creature, self.opponent.active_creature, self.player_action)
        elif self.foe_action:
            self.execute_skill(self.opponent.active_creature, self.player.active_creature, self.foe_action)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        raw_damage = self.calculate_raw_damage(attacker, defender, skill)
        final_damage = self.apply_type_effectiveness(skill, defender, raw_damage)
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! It dealt {final_damage} damage.")

    def calculate_raw_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            return max(0, attacker.attack + skill.base_damage - defender.defense)
        else:
            return max(0, int((attacker.sp_attack / defender.sp_defense) * skill.base_damage))

    def apply_type_effectiveness(self, skill: Skill, defender: Creature, raw_damage: int) -> int:
        effectiveness = 1.0
        if skill.skill_type == "fire" and defender.creature_type == "leaf":
            effectiveness = 2.0
        elif skill.skill_type == "water" and defender.creature_type == "fire":
            effectiveness = 2.0
        elif skill.skill_type == "leaf" and defender.creature_type == "water":
            effectiveness = 2.0
        elif skill.skill_type == "fire" and defender.creature_type == "water":
            effectiveness = 0.5
        elif skill.skill_type == "water" and defender.creature_type == "leaf":
            effectiveness = 0.5
        elif skill.skill_type == "leaf" and defender.creature_type == "fire":
            effectiveness = 0.5
        return int(raw_damage * effectiveness)

    def check_knockouts(self):
        if self.player.active_creature.hp == 0:
            self._show_text(self.player, f"{self.player.active_creature.display_name} is knocked out!")
            self.swap_creature(self.player)
        if self.opponent.active_creature.hp == 0:
            self._show_text(self.player, f"{self.opponent.active_creature.display_name} is knocked out!")
            self.swap_creature(self.opponent)

    def swap_creature(self, player: Player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if available_creatures:
            swap_choice = self._wait_for_choice(player, [SelectThing(creature) for creature in available_creatures])
            player.active_creature = swap_choice.thing
        else:
            self._show_text(self.player, f"{player.display_name} has no creatures left!")
            self._quit_whole_game()
