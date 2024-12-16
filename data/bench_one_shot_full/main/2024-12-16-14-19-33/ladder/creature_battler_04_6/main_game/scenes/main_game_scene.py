from mini_game_engine.engine.lib import AbstractGameScene, Button, DictionaryChoice
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        
        # Reset creature stats
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Type: {self.player_creature.creature_type}

VS

{self.bot.display_name}'s {self.bot_creature.display_name}
HP: {self.bot_creature.hp}/{self.bot_creature.max_hp}
Type: {self.bot_creature.creature_type}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} type, {'physical' if skill.is_physical else 'special'})" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player choice phase
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Bot choice phase  
            bot_skill = self._get_skill_choice(self.bot, self.bot_creature)

            # Resolution phase
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill),
                (self.bot, self.bot_creature, bot_skill)
            )

            # Execute skills
            self._execute_skill(*first)
            if self._check_battle_end():
                break

            if self.player_creature.hp > 0 and self.bot_creature.hp > 0:
                self._execute_skill(*second)
                if self._check_battle_end():
                    break

        # Reset creatures before leaving
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        
        self._transition_to_scene("MainMenuScene")

    def _get_skill_choice(self, player, creature):
        choices = [DictionaryChoice(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _determine_order(self, player_tuple, bot_tuple):
        if player_tuple[1].speed > bot_tuple[1].speed:
            return player_tuple, bot_tuple
        elif player_tuple[1].speed < bot_tuple[1].speed:
            return bot_tuple, player_tuple
        else:
            return random.sample([player_tuple, bot_tuple], 2)

    def _calculate_damage(self, attacker_creature, defender_creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender_creature.creature_type)
        
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

    def _execute_skill(self, attacker, attacker_creature, skill):
        if attacker == self.player:
            defender = self.bot
            defender_creature = self.bot_creature
        else:
            defender = self.player
            defender_creature = self.player_creature

        damage = self._calculate_damage(attacker_creature, defender_creature, skill)
        defender_creature.hp = max(0, defender_creature.hp - damage)

        effectiveness = "super effective!" if self._get_type_multiplier(skill.skill_type, defender_creature.creature_type) > 1 else \
                       "not very effective..." if self._get_type_multiplier(skill.skill_type, defender_creature.creature_type) < 1 else ""
        
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}! {effectiveness}")
        self._show_text(defender, f"{attacker_creature.display_name} used {skill.display_name}! {effectiveness}")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._show_text(self.bot, "You won!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._show_text(self.bot, "You lost!")
            return True
        return False
