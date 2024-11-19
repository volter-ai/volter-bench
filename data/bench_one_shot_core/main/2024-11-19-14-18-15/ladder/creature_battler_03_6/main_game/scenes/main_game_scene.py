from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.type_effectiveness = {
            "fire": {"water": 0.5, "leaf": 2.0},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5},
            "normal": {}
        }

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self.get_skill_choice(self.player, self.player_creature)
            
            # Opponent Choice Phase
            opponent_skill = self.get_skill_choice(self.opponent, self.opponent_creature)

            # Resolution Phase
            first, second = self.determine_order(
                (self.player, self.player_creature, player_skill),
                (self.opponent, self.opponent_creature, opponent_skill)
            )

            # Execute moves in order
            for attacker, creature, skill in [first, second]:
                if attacker == self.player:
                    defender_creature = self.opponent_creature
                else:
                    defender_creature = self.player_creature

                damage = self.calculate_damage(skill, creature, defender_creature)
                defender_creature.hp -= damage

                self._show_text(self.player, 
                    f"{creature.display_name} used {skill.display_name}! Dealt {damage} damage!")

                if defender_creature.hp <= 0:
                    winner = "You" if attacker == self.player else "Opponent"
                    self._show_text(self.player, f"{winner} won the battle!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def get_skill_choice(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills 
                   if skill.display_name == choice.display_name)

    def determine_order(self, player_data, opponent_data):
        player_creature = player_data[1]
        opponent_creature = opponent_data[1]
        
        if player_creature.speed > opponent_creature.speed:
            return player_data, opponent_data
        elif player_creature.speed < opponent_creature.speed:
            return opponent_data, player_data
        else:
            return random.choice([(player_data, opponent_data), 
                                (opponent_data, player_data)])

    def calculate_damage(self, skill, attacker, defender):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Get effectiveness multiplier
        multiplier = 1.0
        if skill.skill_type in self.type_effectiveness:
            multiplier = self.type_effectiveness[skill.skill_type].get(
                defender.creature_type, 1.0)
            
        return int(raw_damage * multiplier)
