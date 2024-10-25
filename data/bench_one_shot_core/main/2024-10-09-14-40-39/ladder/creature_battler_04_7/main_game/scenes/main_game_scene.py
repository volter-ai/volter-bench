from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.get_active_creature(self.player)
        self.opponent_creature = self.get_active_creature(self.opponent)

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Your turn! Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appeared!")
        
        while True:
            # Player turn
            player_skill = self.player_turn()
            
            # Opponent turn
            opponent_skill = self.opponent_turn()
            
            # Resolve turn
            self.resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            if self.check_battle_end():
                break

        # Reset creatures' state before transitioning out
        self.reset_creatures_state()

    def player_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolve_turn(self, player_skill, opponent_skill):
        first, second = self.determine_turn_order(player_skill, opponent_skill)
        self.execute_skill(*first)
        if self.check_battle_end():
            return
        self.execute_skill(*second)

    def determine_turn_order(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player_creature, player_skill, self.opponent_creature), (self.opponent_creature, opponent_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent_creature, opponent_skill, self.player_creature), (self.player_creature, player_skill, self.opponent_creature)
        else:
            if random.random() < 0.5:
                return (self.player_creature, player_skill, self.opponent_creature), (self.opponent_creature, opponent_skill, self.player_creature)
            else:
                return (self.opponent_creature, opponent_skill, self.player_creature), (self.player_creature, player_skill, self.opponent_creature)

    def execute_skill(self, attacker: Creature, skill: Skill, defender: Creature):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = round(weakness_factor * raw_damage)
        
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name}'s {skill.display_name} dealt {final_damage} damage to {defender.display_name}!")

    def calculate_weakness_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1
        elif skill_type == "fire":
            if defender_type == "leaf":
                return 2
            elif defender_type == "water":
                return 0.5
        elif skill_type == "water":
            if defender_type == "fire":
                return 2
            elif defender_type == "leaf":
                return 0.5
        elif skill_type == "leaf":
            if defender_type == "water":
                return 2
            elif defender_type == "fire":
                return 0.5
        return 1

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted. You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted. You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def get_active_creature(self, player: Player) -> Creature:
        return player.creatures[0]  # For now, we'll always use the first creature

    def reset_creatures_state(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
