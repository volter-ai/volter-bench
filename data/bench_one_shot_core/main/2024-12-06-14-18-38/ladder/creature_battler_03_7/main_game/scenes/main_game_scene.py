from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        while True:
            # Player phase
            self._show_text(self.player, "Your turn!")
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing

            # Opponent phase
            self._show_text(self.opponent, "Opponent's turn!")
            opponent_skill = self._wait_for_choice(self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]).thing

            # Resolution phase
            first, second = self.determine_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            # Execute moves
            self.execute_skill(*first)
            if self.check_battle_end():
                return

            self.execute_skill(*second)
            if self.check_battle_end():
                return

    def determine_order(self, move1, move2):
        p1, c1, _ = move1
        p2, c2, _ = move2
        if c1.speed > c2.speed:
            return move1, move2
        elif c2.speed > c1.speed:
            return move2, move1
        else:
            return random.choice([(move1, move2), (move2, move1)])

    def calculate_damage(self, attacker_creature, skill, defender_creature):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender_creature.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)

    def execute_skill(self, attacker, attacker_creature, skill):
        if attacker == self.player:
            defender = self.opponent
            defender_creature = self.opponent_creature
        else:
            defender = self.player
            defender_creature = self.player_creature

        damage = self.calculate_damage(attacker_creature, skill, defender_creature)
        defender_creature.hp = max(0, defender_creature.hp - damage)

        self._show_text(self.player, 
            f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name} for {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name} won the battle!")
            self._transition_to_scene("MainMenuScene") 
            return True
        return False
