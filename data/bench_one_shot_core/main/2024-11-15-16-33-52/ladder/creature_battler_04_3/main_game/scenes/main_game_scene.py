from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
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
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.opponent.display_name}'s {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} VS {self.opponent_creature.display_name}")
        
        while True:
            # Player choice phase
            player_choices = [DictionaryChoice(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, player_choices)
            self.queued_skills[self.player.uid] = self.player_creature.skills[player_choices.index(player_choice)]

            # Opponent choice phase
            opponent_choices = [DictionaryChoice(skill.display_name) for skill in self.opponent_creature.skills]
            opponent_choice = self._wait_for_choice(self.opponent, opponent_choices)
            self.queued_skills[self.opponent.uid] = self.opponent_creature.skills[opponent_choices.index(opponent_choice)]

            # Resolution phase
            first, second = self.determine_order()
            
            # Execute skills
            self.execute_skill(first, second)
            if self.check_battle_end():
                break
                
            self.execute_skill(second, first)
            if self.check_battle_end():
                break

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return self.player, self.opponent
        elif self.player_creature.speed < self.opponent_creature.speed:
            return self.opponent, self.player
        else:
            return random.sample([self.player, self.opponent], 2)

    def calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            if attacker.uid == self.player.uid:
                raw_damage = self.player_creature.attack + skill.base_damage - self.opponent_creature.defense
            else:
                raw_damage = self.opponent_creature.attack + skill.base_damage - self.player_creature.defense
        else:
            if attacker.uid == self.player.uid:
                raw_damage = (self.player_creature.sp_attack / self.opponent_creature.sp_defense) * skill.base_damage
            else:
                raw_damage = (self.opponent_creature.sp_attack / self.player_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, 
            self.opponent_creature.creature_type if attacker.uid == self.player.uid else self.player_creature.creature_type)
        
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

    def execute_skill(self, attacker, defender):
        skill = self.queued_skills[attacker.uid]
        damage = self.calculate_damage(attacker, defender, skill)
        
        if attacker.uid == self.player.uid:
            self.opponent_creature.hp = max(0, self.opponent_creature.hp - damage)
            self._show_text(self.player, f"Your {self.player_creature.display_name} used {skill.display_name} for {damage} damage!")
        else:
            self.player_creature.hp = max(0, self.player_creature.hp - damage)
            self._show_text(self.player, f"Opponent's {self.opponent_creature.display_name} used {skill.display_name} for {damage} damage!")

    def check_battle_end(self):
        battle_ended = False
        
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            battle_ended = True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            battle_ended = True
            
        if battle_ended:
            # Reset creature states before transitioning
            for creature in self.player.creatures:
                creature.hp = creature.max_hp
            for creature in self.opponent.creatures:
                creature.hp = creature.max_hp
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
