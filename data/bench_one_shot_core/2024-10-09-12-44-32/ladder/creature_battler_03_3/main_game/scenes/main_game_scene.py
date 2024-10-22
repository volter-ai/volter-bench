import random

from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.reset_creatures()

    def reset_creatures(self):
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Your creature's skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}

Opponent's creature's skills:
{', '.join([skill.display_name for skill in self.opponent_creature.skills])}

Your turn! Choose a skill:
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

        # After the battle ends, transition back to the main menu
        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def opponent_turn(self):
        return random.choice(self.opponent_creature.skills)

    def resolve_turn(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            self.execute_skill(self.player_creature, self.opponent_creature, player_skill)
            if self.opponent_creature.hp > 0:
                self.execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            self.execute_skill(self.opponent_creature, self.player_creature, opponent_skill)
            if self.player_creature.hp > 0:
                self.execute_skill(self.player_creature, self.opponent_creature, player_skill)
        else:
            # Equal speed, randomly decide who goes first
            first, second = random.sample([
                (self.player_creature, self.opponent_creature, player_skill),
                (self.opponent_creature, self.player_creature, opponent_skill)
            ], 2)
            
            self.execute_skill(first[0], first[1], first[2])
            if first[1].hp > 0:
                self.execute_skill(second[0], second[1], second[2])

    def execute_skill(self, attacker, defender, skill):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * weakness_factor)
        defender.hp = max(0, defender.hp - final_damage)
        
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name} took {final_damage} damage!")

    def calculate_weakness_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1  # Normal type is neither effective nor ineffective against any type
        elif skill_type == defender_type:
            return 1
        elif (skill_type == "fire" and defender_type == "leaf") or \
             (skill_type == "water" and defender_type == "fire") or \
             (skill_type == "leaf" and defender_type == "water"):
            return 2
        elif (skill_type == "fire" and defender_type == "water") or \
             (skill_type == "water" and defender_type == "leaf") or \
             (skill_type == "leaf" and defender_type == "fire"):
            return 0.5
        else:
            return 1

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
