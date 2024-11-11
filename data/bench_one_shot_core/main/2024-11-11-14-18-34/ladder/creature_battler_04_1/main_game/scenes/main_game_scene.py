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
            choice = self._wait_for_choice(
                self.opponent,
                [SelectThing(skill, label=skill.display_name) for skill in self.opponent_creature.skills]
            )
            self.opponent_chosen_skill = choice.thing

            # Resolution phase
            first, second = self.determine_order()
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
            if attacker == self.player:
                raw_damage = self.player_creature.attack + skill.base_damage - self.opponent_creature.defense
            else:
                raw_damage = self.opponent_creature.attack + skill.base_damage - self.player_creature.defense
        else:
            if attacker == self.player:
                raw_damage = (self.player_creature.sp_attack / self.opponent_creature.sp_defense) * skill.base_damage
            else:
                raw_damage = (self.opponent_creature.sp_attack / self.player_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creatures[0].creature_type)
        
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

    def execute_turn(self, attacker):
        defender = self.opponent if attacker == self.player else self.player
        skill = self.player_chosen_skill if attacker == self.player else self.opponent_chosen_skill
        
        damage = self.calculate_damage(attacker, defender, skill)
        
        if defender == self.player:
            self.player_creature.hp = max(0, self.player_creature.hp - damage)
        else:
            self.opponent_creature.hp = max(0, self.opponent_creature.hp - damage)

        self._show_text(self.player, f"{attacker.display_name}'s {skill.display_name} dealt {damage} damage!")

    def reset_creature_states(self):
        """Reset all creatures back to their initial states"""
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            self.reset_creature_states()
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            self.reset_creature_states()
            self._transition_to_scene("MainMenuScene") 
            return True
        return False
