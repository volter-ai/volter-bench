from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.queued_skills = {}  # Will store {player_uid: skill}

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player Choice Phase
            self.player_choice_phase()
            
            # Opponent Choice Phase  
            self.opponent_choice_phase()
            
            # Resolution Phase
            winner = self.resolution_phase()
            if winner:
                if winner == self.player:
                    self._show_text(self.player, "You won!")
                else:
                    self._show_text(self.player, "You lost!")
                self._quit_whole_game()

    def player_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        selected_skill = next(s for s in self.player_creature.skills if s.display_name == choice.display_name)
        self.queued_skills[self.player.uid] = selected_skill

    def opponent_choice_phase(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        selected_skill = next(s for s in self.opponent_creature.skills if s.display_name == choice.display_name)
        self.queued_skills[self.opponent.uid] = selected_skill

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        # Type effectiveness
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf":
                multiplier = 2.0
            elif defender_creature.creature_type == "water":
                multiplier = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire":
                multiplier = 2.0
            elif defender_creature.creature_type == "leaf":
                multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water":
                multiplier = 2.0
            elif defender_creature.creature_type == "fire":
                multiplier = 0.5
                
        return int(raw_damage * multiplier)

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
            if attacker == self.player:
                attacker_creature = self.player_creature
                defender_creature = self.opponent_creature
            else:
                attacker_creature = self.opponent_creature
                defender_creature = self.player_creature

            skill = self.queued_skills[attacker.uid]
            damage = self.calculate_damage(attacker_creature, defender_creature, skill)
            defender_creature.hp -= damage
            
            self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name} for {damage} damage!")
            
            if defender_creature.hp <= 0:
                return self.player if defender_creature == self.opponent_creature else self.opponent

        return None
