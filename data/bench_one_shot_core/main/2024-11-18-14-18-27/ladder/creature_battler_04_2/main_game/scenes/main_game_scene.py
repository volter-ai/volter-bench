from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.phase = "player_choice"
        self.player_skill = None
        self.bot_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Phase: {self.phase}"""

    def run(self):
        while True:
            if self.phase == "player_choice":
                self._show_text(self.player, "Choose your skill!")
                choices = [SelectThing(skill) for skill in self.player_creature.skills]
                self.player_skill = self._wait_for_choice(self.player, choices).thing
                self.phase = "bot_choice"

            elif self.phase == "bot_choice":
                self.bot_skill = self._wait_for_choice(self.bot, 
                    [SelectThing(skill) for skill in self.bot_creature.skills]).thing
                self.phase = "resolution"

            elif self.phase == "resolution":
                first, second = self.determine_order()
                self.execute_turn(first)
                if self.check_battle_end():
                    return
                self.execute_turn(second)
                if self.check_battle_end():
                    return
                self.phase = "player_choice"

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.player_skill), (self.bot, self.bot_skill)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot, self.bot_skill), (self.player, self.player_skill)
        else:
            actors = [(self.player, self.player_skill), (self.bot, self.bot_skill)]
            random.shuffle(actors)
            return actors[0], actors[1]

    def calculate_damage(self, attacker, skill, defender):
        if skill.is_physical:
            raw_damage = (attacker.attack + skill.base_damage - defender.defense)
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_factor)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def execute_turn(self, actor_data):
        actor, skill = actor_data
        attacker = self.player_creature if actor == self.player else self.bot_creature
        defender = self.bot_creature if actor == self.player else self.player_creature
        
        damage = self.calculate_damage(attacker, skill, defender)
        defender.hp = max(0, defender.hp - damage)
        
        self._show_text(self.player, 
            f"{actor.display_name}'s {attacker.display_name} used {skill.display_name}! Dealt {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            # Reset HP directly instead of using a method
            self.player_creature.hp = self.player_creature.max_hp
            self.bot_creature.hp = self.bot_creature.max_hp
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            # Reset HP directly instead of using a method
            self.player_creature.hp = self.player_creature.max_hp
            self.bot_creature.hp = self.bot_creature.max_hp
            self._transition_to_scene("MainMenuScene")
            return True
        return False
