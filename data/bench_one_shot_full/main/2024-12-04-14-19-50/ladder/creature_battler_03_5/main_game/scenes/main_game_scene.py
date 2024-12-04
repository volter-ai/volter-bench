from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.queued_skills = {}

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} type)" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player phase
            self._show_text(self.player, "Your turn! Choose a skill:")
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing

            # Opponent phase
            self._show_text(self.opponent, "Choose a skill:")
            opponent_skill = self._wait_for_choice(self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]).thing

            # Resolution phase
            first, second = self.determine_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            # Execute skills
            for attacker, creature, skill in [first, second]:
                if attacker == self.player:
                    defender_creature = self.opponent_creature
                else:
                    defender_creature = self.player_creature

                damage = self.calculate_damage(skill, creature, defender_creature)
                defender_creature.hp -= damage

                self._show_text(self.player, 
                    f"{creature.display_name} used {skill.display_name} for {damage} damage!")
                self._show_text(self.opponent,
                    f"{creature.display_name} used {skill.display_name} for {damage} damage!")

                if defender_creature.hp <= 0:
                    winner = self.player if defender_creature == self.opponent_creature else self.opponent
                    self._show_text(self.player, f"{winner.display_name} wins!")
                    self._show_text(self.opponent, f"{winner.display_name} wins!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def determine_order(self, p1_data, p2_data):
        p1_speed = p1_data[1].speed
        p2_speed = p2_data[1].speed
        
        if p1_speed > p2_speed:
            return p1_data, p2_data
        elif p2_speed > p1_speed:
            return p2_data, p1_data
        else:
            return random.sample([p1_data, p2_data], 2)

    def calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense

        # Calculate type multiplier
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)

        # Calculate final damage
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }

        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)
