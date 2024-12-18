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
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, f"A battle begins between {self.player.display_name} and {self.opponent.display_name}!")
        
        while True:
            # Player Choice Phase
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills])
            self.queued_skills[self.player.uid] = player_skill.thing

            # Opponent Choice Phase  
            opponent_skill = self._wait_for_choice(self.opponent,
                [SelectThing(skill) for skill in self.opponent_creature.skills])
            self.queued_skills[self.opponent.uid] = opponent_skill.thing

            # Resolution Phase
            first, second = self._determine_order()
            
            # Execute first skill
            damage = self._calculate_damage(first[0], first[1])
            self._show_text(self.player, f"{first[0].display_name} uses {first[2].display_name}!")
            self._show_text(self.player, f"It deals {damage} damage!")
            first[1].hp -= damage
            
            if first[1].hp <= 0:
                self._handle_battle_end(first[1] == self.player_creature)
                return

            # Execute second skill
            damage = self._calculate_damage(second[0], second[1])
            self._show_text(self.player, f"{second[0].display_name} uses {second[2].display_name}!")
            self._show_text(self.player, f"It deals {damage} damage!")
            second[1].hp -= damage

            if second[1].hp <= 0:
                self._handle_battle_end(second[1] == self.player_creature)
                return

    def _determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            first = (self.player_creature, self.opponent_creature, self.queued_skills[self.player.uid])
            second = (self.opponent_creature, self.player_creature, self.queued_skills[self.opponent.uid])
        elif self.player_creature.speed < self.opponent_creature.speed:
            first = (self.opponent_creature, self.player_creature, self.queued_skills[self.opponent.uid])
            second = (self.player_creature, self.opponent_creature, self.queued_skills[self.player.uid])
        else:
            if random.random() < 0.5:
                first = (self.player_creature, self.opponent_creature, self.queued_skills[self.player.uid])
                second = (self.opponent_creature, self.player_creature, self.queued_skills[self.opponent.uid])
            else:
                first = (self.opponent_creature, self.player_creature, self.queued_skills[self.opponent.uid])
                second = (self.player_creature, self.opponent_creature, self.queued_skills[self.player.uid])
        return first, second

    def _calculate_damage(self, attacker, defender):
        attacker_id = self.player.uid if attacker == self.player_creature else self.opponent.uid
        skill = self.queued_skills[attacker_id]
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Calculate type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _handle_battle_end(self, player_lost):
        if player_lost:
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")
        self._transition_to_scene("MainMenuScene")
