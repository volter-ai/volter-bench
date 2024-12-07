from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.queued_skills = {}  # Will store uid -> skill mappings

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A battle begins between {self.player.display_name} and {self.opponent.display_name}!")
        
        while True:
            # Player choice phase
            self._show_text(self.player, "Choose your skill!")
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]).thing
            self.queued_skills[self.player.uid] = player_skill

            # Opponent choice phase
            opponent_skill = self._wait_for_choice(self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills]).thing
            self.queued_skills[self.opponent.uid] = opponent_skill

            # Resolution phase
            first, second = self.determine_order()
            
            # Execute skills
            for attacker in [first, second]:
                defender = self.opponent if attacker == self.player else self.player
                attacker_creature = self.player_creature if attacker == self.player else self.opponent_creature
                defender_creature = self.opponent_creature if attacker == self.player else self.player_creature
                
                skill = self.queued_skills[attacker.uid]
                damage = self.calculate_damage(skill, attacker_creature, defender_creature)
                
                defender_creature.hp = max(0, defender_creature.hp - damage)
                self._show_text(self.player, 
                    f"{attacker.display_name}'s {attacker_creature.display_name} used {skill.display_name} for {damage} damage!")

                if defender_creature.hp <= 0:
                    winner = attacker
                    self._show_text(self.player, 
                        f"{winner.display_name} wins! {defender_creature.display_name} was defeated!")
                    # Reset HP
                    self.player_creature.hp = self.player_creature.max_hp
                    self.opponent_creature.hp = self.opponent_creature.max_hp
                    self._transition_to_scene("MainMenuScene")
                    return

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return self.player, self.opponent
        elif self.opponent_creature.speed > self.player_creature.speed:
            return self.opponent, self.player
        else:
            return random.sample([self.player, self.opponent], 2)

    def calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)
