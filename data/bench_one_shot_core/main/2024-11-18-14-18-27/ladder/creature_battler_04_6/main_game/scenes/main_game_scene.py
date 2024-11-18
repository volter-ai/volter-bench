from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, create_from_game_database
from main_game.models import Skill, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.phase = "player_choice"
        self.queued_skills = {}  # Will store prototype_ids as keys

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
VS
{self.bot.display_name}'s {self.bot_creature.display_name} (HP: {self.bot_creature.hp}/{self.bot_creature.max_hp})

Phase: {self.phase}
"""

    def run(self):
        while True:
            if self.phase == "player_choice":
                self._show_text(self.player, "Choose your skill!")
                skill = self._wait_for_choice(self.player, 
                    [SelectThing(skill) for skill in self.player_creature.skills])
                self.queued_skills[self.player.prototype_id] = skill.thing
                self.phase = "foe_choice"

            elif self.phase == "foe_choice":
                self._show_text(self.bot, "Bot choosing skill...")
                skill = self._wait_for_choice(self.bot,
                    [SelectThing(skill) for skill in self.bot_creature.skills])
                self.queued_skills[self.bot.prototype_id] = skill.thing
                self.phase = "resolution"

            else: # resolution phase
                first, second = self._determine_order()
                self._execute_turn(first)
                if self._check_battle_end():
                    return
                self._execute_turn(second)
                if self._check_battle_end():
                    return
                
                self.queued_skills = {}
                self.phase = "player_choice"

    def _determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return self.player, self.bot
        elif self.bot_creature.speed > self.player_creature.speed:
            return self.bot, self.player
        else:
            return random.sample([self.player, self.bot], 2)

    def _execute_turn(self, attacker):
        defender = self.bot if attacker == self.player else self.player
        atk_creature = self.player_creature if attacker == self.player else self.bot_creature
        def_creature = self.bot_creature if attacker == self.player else self.player_creature
        
        skill = self.queued_skills[attacker.prototype_id]
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = atk_creature.attack + skill.base_damage - def_creature.defense
        else:
            raw_damage = (atk_creature.sp_attack / def_creature.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = self._get_effectiveness(skill.skill_type, def_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        def_creature.hp = max(0, def_creature.hp - final_damage)
        
        self._show_text(attacker, f"{atk_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{def_creature.display_name} took {final_damage} damage!")

    def _get_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def _reset_creatures(self):
        # Reset player creatures by creating fresh instances
        for i, creature in enumerate(self.player.creatures):
            self.player.creatures[i] = create_from_game_database(creature.prototype_id, Creature)
        
        # Reset bot creatures by creating fresh instances
        for i, creature in enumerate(self.bot.creatures):
            self.bot.creatures[i] = create_from_game_database(creature.prototype_id, Creature)

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._reset_creatures()  # Reset before transitioning
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._reset_creatures()  # Reset before transitioning
            self._transition_to_scene("MainMenuScene") 
            return True
        return False
