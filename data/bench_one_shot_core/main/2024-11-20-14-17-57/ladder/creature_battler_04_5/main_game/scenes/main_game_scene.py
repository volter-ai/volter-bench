from mini_game_engine.engine.lib import AbstractGameScene, Button
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
Your {self.player_creature.display_name}: {self.player_creature.hp}/{self.player_creature.max_hp} HP
Opponent's {self.opponent_creature.display_name}: {self.opponent_creature.hp}/{self.opponent_creature.max_hp} HP

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player Choice Phase
            choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, choices)
            self.player_chosen_skill = self.player_creature.skills[choices.index(player_choice)]

            # Opponent Choice Phase
            opponent_choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
            opponent_choice = self._wait_for_choice(self.opponent, opponent_choices)
            self.opponent_chosen_skill = self.opponent_creature.skills[opponent_choices.index(opponent_choice)]

            # Resolution Phase
            first, second = self.determine_order()
            
            # Execute first attack
            damage = self.calculate_damage(first[0], first[1], first[2], first[3])
            first[3].hp -= damage
            self._show_text(self.player, f"{first[0].display_name} used {first[1].display_name} for {damage} damage!")
            
            if first[3].hp <= 0:
                self.handle_battle_end(first[3] == self.opponent_creature)
                return

            # Execute second attack
            damage = self.calculate_damage(second[0], second[1], second[2], second[3])
            second[3].hp -= damage
            self._show_text(self.player, f"{second[0].display_name} used {second[1].display_name} for {damage} damage!")
            
            if second[3].hp <= 0:
                self.handle_battle_end(second[3] == self.opponent_creature)
                return

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return (self.player_creature, self.player_chosen_skill, self.opponent_creature, self.opponent_creature), \
                   (self.opponent_creature, self.opponent_chosen_skill, self.player_creature, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            return (self.opponent_creature, self.opponent_chosen_skill, self.player_creature, self.player_creature), \
                   (self.player_creature, self.player_chosen_skill, self.opponent_creature, self.opponent_creature)
        else:
            if random.random() < 0.5:
                return (self.player_creature, self.player_chosen_skill, self.opponent_creature, self.opponent_creature), \
                       (self.opponent_creature, self.opponent_chosen_skill, self.player_creature, self.player_creature)
            else:
                return (self.opponent_creature, self.opponent_chosen_skill, self.player_creature, self.player_creature), \
                       (self.player_creature, self.player_chosen_skill, self.opponent_creature, self.opponent_creature)

    def calculate_damage(self, attacker, skill, defender, target):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, target.creature_type)
        
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

    def handle_battle_end(self, player_won):
        if player_won:
            self._show_text(self.player, "You won the battle!")
        else:
            self._show_text(self.player, "You lost the battle!")
        
        # Reset creature states
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp
            
        self._transition_to_scene("MainMenuScene")
