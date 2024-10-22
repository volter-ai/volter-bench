from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Choose a skill:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.opponent.display_name} appeared!")
        while True:
            # Player Choice Phase
            player_skill = self.player_turn()
            
            # Foe Choice Phase
            opponent_skill = self.opponent_turn()
            
            # Resolution Phase
            self.resolve_turn(player_skill, opponent_skill)
            
            if self.check_battle_end():
                break

    def player_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_turn(self):
        choices = [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolve_turn(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self.execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
            if self.opponent_creature.hp > 0:
                self.execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self.execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
            if self.player_creature.hp > 0:
                self.execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
        else:
            # If speeds are equal, randomly decide who goes first
            if random.choice([True, False]):
                self.execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)
                if self.opponent_creature.hp > 0:
                    self.execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
            else:
                self.execute_skill(self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
                if self.player_creature.hp > 0:
                    self.execute_skill(self.player, self.player_creature, player_skill, self.opponent_creature)

    def execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        effectiveness = "It's super effective!" if weakness_factor > 1 else "It's not very effective..." if weakness_factor < 1 else ""
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}! {effectiveness}")
        self._show_text(attacker, f"{defender_creature.display_name} took {final_damage} damage!")

    def calculate_weakness_factor(self, skill_type, defender_type):
        if skill_type.lower() == "normal":
            return 1  # Normal type is neither effective nor ineffective against any other types
        
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self.end_battle(f"{self.player.display_name}'s {self.player_creature.display_name} fainted! You lose!")
            return True
        elif self.opponent_creature.hp <= 0:
            self.end_battle(f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted! You win!")
            return True
        return False

    def end_battle(self, message):
        self._show_text(self.player, message)
        self._transition_to_scene("MainMenuScene")
