from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_player_skill = None
        self.queued_bot_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player choice phase
            skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            self.queued_player_skill = self.player_creature.skills[skill_choices.index(player_choice)]

            # Bot choice phase
            bot_skill_choices = [Button(skill.display_name) for skill in self.bot_creature.skills]
            bot_choice = self._wait_for_choice(self.bot, bot_skill_choices)
            self.queued_bot_skill = self.bot_creature.skills[bot_skill_choices.index(bot_choice)]

            # Resolution phase
            first, second = self.determine_order()
            self.resolve_skill(first[0], first[1], first[2], first[3])
            
            if self.check_battle_end():
                break
                
            self.resolve_skill(second[0], second[1], second[2], second[3])
            
            if self.check_battle_end():
                break

        # Reset creatures before leaving
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def determine_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.player_creature, self.queued_player_skill, self.bot_creature), \
                   (self.bot, self.bot_creature, self.queued_bot_skill, self.player_creature)
        elif self.player_creature.speed < self.bot_creature.speed:
            return (self.bot, self.bot_creature, self.queued_bot_skill, self.player_creature), \
                   (self.player, self.player_creature, self.queued_player_skill, self.bot_creature)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_creature, self.queued_player_skill, self.bot_creature), \
                       (self.bot, self.bot_creature, self.queued_bot_skill, self.player_creature)
            else:
                return (self.bot, self.bot_creature, self.queued_bot_skill, self.player_creature), \
                       (self.player, self.player_creature, self.queued_player_skill, self.bot_creature)

    def resolve_skill(self, attacker, attacker_creature, skill, defender_creature):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        factor = self.get_type_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(factor * raw_damage)
        
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"Dealt {final_damage} damage!")

    def get_type_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
