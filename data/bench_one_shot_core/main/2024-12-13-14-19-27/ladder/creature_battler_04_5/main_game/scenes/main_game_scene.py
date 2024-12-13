from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.queued_skills = {}

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player Choice Phase
            self.player_choice_phase()
            
            # Opponent Choice Phase  
            self.opponent_choice_phase()
            
            # Resolution Phase
            if self.resolution_phase():
                break

        # Reset creatures before leaving
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.queued_skills[self.player.uid] = choice.thing

    def opponent_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        self.queued_skills[self.opponent.uid] = choice.thing

    def resolution_phase(self):
        # Determine order
        first = self.player
        second = self.opponent
        if self.opponent_creature.speed > self.player_creature.speed:
            first, second = second, first
        elif self.opponent_creature.speed == self.player_creature.speed:
            if random.random() < 0.5:
                first, second = second, first

        # Execute skills
        for attacker in [first, second]:
            defender = self.opponent if attacker == self.player else self.player
            attacker_creature = self.player_creature if attacker == self.player else self.opponent_creature
            defender_creature = self.opponent_creature if attacker == self.player else self.player_creature
            
            skill = self.queued_skills[attacker.uid]
            damage = self.calculate_damage(skill, attacker_creature, defender_creature)
            
            defender_creature.hp = max(0, defender_creature.hp - damage)
            self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name} for {damage} damage!")
            
            if defender_creature.hp <= 0:
                winner = "You win!" if defender == self.opponent else "You lose!"
                self._show_text(self.player, f"{defender_creature.display_name} fainted! {winner}")
                return True

        self.queued_skills.clear()
        return False

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
            
        effectiveness_map = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        
        return effectiveness_map.get((skill_type, defender_type), 1.0)
