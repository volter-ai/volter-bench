from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        
        # Reset creatures
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Calculate type effectiveness
        effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf":
                effectiveness = 2.0
            elif defender_creature.creature_type == "water":
                effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire":
                effectiveness = 2.0
            elif defender_creature.creature_type == "leaf":
                effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water":
                effectiveness = 2.0
            elif defender_creature.creature_type == "fire":
                effectiveness = 0.5

        return int(raw_damage * effectiveness)

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._wait_for_choice(self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills])
            
            # Bot choice phase
            bot_skill = self._wait_for_choice(self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills])

            # Resolution phase
            first = self.player_creature if self.player_creature.speed > self.bot_creature.speed else self.bot_creature
            second = self.bot_creature if first == self.player_creature else self.player_creature
            first_skill = player_skill.thing if first == self.player_creature else bot_skill.thing
            second_skill = bot_skill.thing if first == self.player_creature else player_skill.thing

            # If speeds are equal, randomize order
            if self.player_creature.speed == self.bot_creature.speed:
                if random.random() < 0.5:
                    first, second = second, first
                    first_skill, second_skill = second_skill, first_skill

            # Execute first attack
            damage = self.calculate_damage(first, second, first_skill)
            second.hp -= damage
            self._show_text(self.player, f"{first.display_name} used {first_skill.display_name} for {damage} damage!")

            # Check if battle ended
            if second.hp <= 0:
                winner = self.player if first == self.player_creature else self.bot
                self._show_text(self.player, f"{winner.display_name} wins!")
                return self._transition_to_scene("MainMenuScene")

            # Execute second attack
            damage = self.calculate_damage(second, first, second_skill)
            first.hp -= damage
            self._show_text(self.player, f"{second.display_name} used {second_skill.display_name} for {damage} damage!")

            # Check if battle ended
            if first.hp <= 0:
                winner = self.player if second == self.player_creature else self.bot
                self._show_text(self.player, f"{winner.display_name} wins!")
                return self._transition_to_scene("MainMenuScene")
