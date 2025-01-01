from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_action = None
        self.opponent_action = None

    def __str__(self):
        return f"""===Main Game===
Player: {self.player.display_name}
Active Creature: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
Opponent: {self.opponent.display_name}
Active Creature: {self.opponent.active_creature.display_name} (HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp})
"""

    def run(self):
        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()
            if self.check_battle_end():
                break

    def player_choice_phase(self):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choices = [attack_button, swap_button]
        choice = self._wait_for_choice(self.player, choices)

        if choice == attack_button:
            self.player_action = self.attack_phase(self.player)
        elif choice == swap_button:
            self.player_action = self.swap_phase(self.player)

    def foe_choice_phase(self):
        # Simulate bot choice
        self.opponent_action = self.attack_phase(self.opponent)

    def resolution_phase(self):
        # Resolve actions
        if isinstance(self.player_action, Skill) and isinstance(self.opponent_action, Skill):
            self.resolve_skills(self.player, self.opponent)
        elif isinstance(self.player_action, Creature):
            self.player.active_creature = self.player_action
        elif isinstance(self.opponent_action, Creature):
            self.opponent.active_creature = self.opponent_action

    def attack_phase(self, player: Player):
        skills = player.active_creature.skills
        skill_choices = [SelectThing(skill) for skill in skills]
        choice = self._wait_for_choice(player, skill_choices)
        return choice.thing

    def swap_phase(self, player: Player):
        creatures = [creature for creature in player.creatures if creature.hp > 0 and creature != player.active_creature]
        creature_choices = [SelectThing(creature) for creature in creatures]
        choice = self._wait_for_choice(player, creature_choices)
        return choice.thing

    def resolve_skills(self, player: Player, opponent: Player):
        player_skill = self.player_action
        opponent_skill = self.opponent_action

        player_speed = player.active_creature.speed
        opponent_speed = opponent.active_creature.speed

        if player_speed > opponent_speed or (player_speed == opponent_speed and random.choice([True, False])):
            self.execute_skill(player, opponent, player_skill)
            if opponent.active_creature.hp > 0:
                self.execute_skill(opponent, player, opponent_skill)
        else:
            self.execute_skill(opponent, player, opponent_skill)
            if player.active_creature.hp > 0:
                self.execute_skill(player, opponent, player_skill)

    def execute_skill(self, attacker: Player, defender: Player, skill: Skill):
        raw_damage = self.calculate_raw_damage(attacker.active_creature, defender.active_creature, skill)
        final_damage = self.calculate_final_damage(raw_damage, skill.skill_type, defender.active_creature.creature_type)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)

    def calculate_raw_damage(self, attacker: Creature, defender: Creature, skill: Skill):
        if skill.is_physical:
            return max(0, attacker.attack + skill.base_damage - defender.defense)
        else:
            return max(0, (attacker.sp_attack / defender.sp_defense) * skill.base_damage)

    def calculate_final_damage(self, raw_damage: float, skill_type: str, creature_type: str):
        type_effectiveness = self.get_type_effectiveness(skill_type, creature_type)
        return int(raw_damage * type_effectiveness)

    def get_type_effectiveness(self, skill_type: str, creature_type: str):
        effectiveness = {
            "normal": {},
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)

    def check_battle_end(self):
        if self.player.active_creature.hp == 0:
            if all(creature.hp == 0 for creature in self.player.creatures):
                self._show_text(self.player, "You lost the battle!")
                return True
            else:
                self.player.active_creature = self.swap_phase(self.player)
        if self.opponent.active_creature.hp == 0:
            if all(creature.hp == 0 for creature in self.opponent.creatures):
                self._show_text(self.player, "You won the battle!")
                return True
            else:
                self.opponent.active_creature = self.swap_phase(self.opponent)
        return False
