from mini_game_engine.engine.lib import AbstractGameScene, Button, create_from_game_database
from main_game.models import Player
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}"""

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._get_player_choice()
            
            # Bot choice phase
            bot_skill = self._get_bot_choice()
            
            # Resolution phase
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill),
                (self.bot, self.bot_creature, bot_skill)
            )
            
            # Execute moves in order
            for attacker, attacker_creature, skill in [first, second]:
                defender = self.bot if attacker == self.player else self.player
                defender_creature = self.bot_creature if attacker == self.player else self.player_creature
                
                damage = self._calculate_damage(skill, attacker_creature, defender_creature)
                defender_creature.hp = max(0, defender_creature.hp - damage)
                
                self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
                self._show_text(attacker, f"Dealt {damage} damage!")
                
                if defender_creature.hp <= 0:
                    winner = attacker.display_name
                    self._show_text(self.player, f"{winner} wins!")
                    self._reset_creatures()
                    self._transition_to_scene("MainMenuScene")
                    return

    def _get_player_choice(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return next(skill for skill in self.player_creature.skills if skill.display_name == choice.display_name)

    def _get_bot_choice(self):
        choices = [Button(skill.display_name) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        return next(skill for skill in self.bot_creature.skills if skill.display_name == choice.display_name)

    def _determine_order(self, player_tuple, bot_tuple):
        if player_tuple[1].speed > bot_tuple[1].speed:
            return player_tuple, bot_tuple
        elif bot_tuple[1].speed > player_tuple[1].speed:
            return bot_tuple, player_tuple
        else:
            return random.sample([player_tuple, bot_tuple], 2)

    def _calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        # Apply type effectiveness
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

    def _reset_creatures(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
