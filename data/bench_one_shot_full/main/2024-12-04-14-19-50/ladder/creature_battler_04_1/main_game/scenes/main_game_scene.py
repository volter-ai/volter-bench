from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.player_chosen_skill = None
        self.bot_chosen_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name}" for skill in self.player_creature.skills])}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player choice phase
            skill_choices = [Button(skill.display_name) for skill in self.player_creature.skills]
            player_choice = self._wait_for_choice(self.player, skill_choices)
            self.player_chosen_skill = self.player_creature.skills[skill_choices.index(player_choice)]

            # Bot choice phase
            bot_choice = self._wait_for_choice(self.bot, [Button(skill.display_name) for skill in self.bot_creature.skills])
            self.bot_chosen_skill = self.bot_creature.skills[[s.display_name for s in self.bot_creature.skills].index(bot_choice.display_name)]

            # Resolution phase
            first, second = self.determine_turn_order()
            
            # Execute moves
            self.execute_move(*first)
            if self.check_battle_end():
                break
                
            self.execute_move(*second)
            if self.check_battle_end():
                break

        # Reset creatures before leaving
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def determine_turn_order(self):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player_creature, self.player_chosen_skill, self.bot_creature), (self.bot_creature, self.bot_chosen_skill, self.player_creature)
        elif self.bot_creature.speed > self.player_creature.speed:
            return (self.bot_creature, self.bot_chosen_skill, self.player_creature), (self.player_creature, self.player_chosen_skill, self.bot_creature)
        else:
            if random.random() < 0.5:
                return (self.player_creature, self.player_chosen_skill, self.bot_creature), (self.bot_creature, self.bot_chosen_skill, self.player_creature)
            return (self.bot_creature, self.bot_chosen_skill, self.player_creature), (self.player_creature, self.player_chosen_skill, self.bot_creature)

    def calculate_damage(self, attacker, skill, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)

    def execute_move(self, attacker, skill, defender):
        damage = self.calculate_damage(attacker, skill, defender)
        defender.hp = max(0, defender.hp - damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! Dealt {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
