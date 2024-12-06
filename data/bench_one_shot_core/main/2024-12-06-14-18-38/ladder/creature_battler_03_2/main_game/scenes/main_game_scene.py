from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_chosen_skill = None
        self.opponent_chosen_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}:
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Type: {self.player_creature.creature_type}

{self.opponent.display_name}'s {self.opponent_creature.display_name}:
HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp}
Type: {self.opponent_creature.creature_type}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        # Type effectiveness
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf": multiplier = 2.0
            elif defender_creature.creature_type == "water": multiplier = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire": multiplier = 2.0
            elif defender_creature.creature_type == "leaf": multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water": multiplier = 2.0
            elif defender_creature.creature_type == "fire": multiplier = 0.5

        return int(raw_damage * multiplier)

    def execute_turn(self):
        # Determine order
        creatures = [(self.player_creature, self.player_chosen_skill, self.opponent_creature),
                    (self.opponent_creature, self.opponent_chosen_skill, self.player_creature)]
        
        if self.player_creature.speed != self.opponent_creature.speed:
            creatures.sort(key=lambda x: x[0].speed, reverse=True)
        else:
            random.shuffle(creatures)

        # Execute attacks
        for attacker, skill, defender in creatures:
            damage = self.calculate_damage(attacker, defender, skill)
            defender.hp = max(0, defender.hp - damage)
            self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")
            
            if defender.hp == 0:
                return True
        return False

    def run(self):
        while True:
            # Player choice phase
            choices = [SelectThing(skill) for skill in self.player_creature.skills]
            self.player_chosen_skill = self._wait_for_choice(self.player, choices).thing

            # Opponent choice phase  
            choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
            self.opponent_chosen_skill = self._wait_for_choice(self.opponent, choices).thing

            # Resolution phase
            battle_ended = self.execute_turn()
            
            if battle_ended:
                if self.player_creature.hp == 0:
                    self._show_text(self.player, "You lost!")
                else:
                    self._show_text(self.player, "You won!")
                self._transition_to_scene("MainMenuScene")
                return
