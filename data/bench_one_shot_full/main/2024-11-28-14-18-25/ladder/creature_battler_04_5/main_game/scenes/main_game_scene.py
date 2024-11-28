from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player choice phase
            self._show_text(self.player, "Choose your skill!")
            choice = self._wait_for_choice(
                self.player, 
                [SelectThing(skill, label=skill.display_name) for skill in self.player_creature.skills]
            )
            self.player_chosen_skill = choice.thing

            # Opponent choice phase
            self._show_text(self.opponent, "Choose your skill!")
            choice = self._wait_for_choice(
                self.opponent,
                [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
            )
            self.opponent_chosen_skill = choice.thing

            # Resolution phase
            first, second = self.determine_order()
            
            # Execute skills
            self.execute_turn(first)
            if self.check_battle_end():
                break
                
            self.execute_turn(second)
            if self.check_battle_end():
                break

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player, self.opponent)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent, self.player)
        else:
            return random.choice([(self.player, self.opponent), (self.opponent, self.player)])

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def execute_turn(self, attacker):
        if attacker == self.player:
            attacking_creature = self.player_creature
            defending_creature = self.opponent_creature
            skill = self.player_chosen_skill
        else:
            attacking_creature = self.opponent_creature
            defending_creature = self.player_creature
            skill = self.opponent_chosen_skill

        damage = self.calculate_damage(attacking_creature, defending_creature, skill)
        defending_creature.hp = max(0, defending_creature.hp - damage)
        
        self._show_text(self.player, f"{attacking_creature.display_name} used {skill.display_name} for {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene") 
            return True
        return False
