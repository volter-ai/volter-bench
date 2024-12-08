from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_choice = None
        self.bot_choice = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.bot_creature.display_name}")
        
        while True:
            # Player Choice Phase
            self.player_choice = self._get_skill_choice(self.player, self.player_creature)
            
            # Bot Choice Phase
            self.bot_choice = self._get_skill_choice(self.bot, self.bot_creature)
            
            # Resolution Phase
            self._resolve_turn()
            
            # Check for battle end
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")

    def _get_skill_choice(self, player, creature):
        choices = [DictionaryChoice(skill.display_name) for skill in creature.skills]
        for choice, skill in zip(choices, creature.skills):
            choice.value = {"skill": skill}
        return self._wait_for_choice(player, choices)

    def _resolve_turn(self):
        player_skill = self.player_choice.value["skill"]
        bot_skill = self.bot_choice.value["skill"]

        # Determine order
        first = self.player_creature if self.player_creature.speed > self.bot_creature.speed else self.bot_creature
        second = self.bot_creature if first == self.player_creature else self.player_creature
        first_skill = player_skill if first == self.player_creature else bot_skill
        second_skill = bot_skill if first == self.player_creature else player_skill

        # If speeds are equal, randomize
        if self.player_creature.speed == self.bot_creature.speed:
            if random.random() < 0.5:
                first, second = second, first
                first_skill, second_skill = second_skill, first_skill

        # Execute skills
        self._execute_skill(first, second, first_skill)
        if second.hp > 0:
            self._execute_skill(second, first, second_skill)

    def _execute_skill(self, attacker, defender, skill):
        # Calculate raw damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Calculate type multiplier
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        # Calculate final damage
        final_damage = int(raw_damage * multiplier)
        final_damage = max(1, final_damage)  # Minimum 1 damage
        
        # Apply damage
        defender.hp -= final_damage
        defender.hp = max(0, defender.hp)  # Don't go below 0
        
        # Show result
        effectiveness = "It's super effective!" if multiplier > 1 else "It's not very effective..." if multiplier < 1 else ""
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! {effectiveness} Dealt {final_damage} damage!")

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
