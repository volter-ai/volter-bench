from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{[skill.display_name for skill in self.player_creature.skills]}
"""

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player_creature.display_name} vs {self.bot_creature.display_name}")
        
        while not self.battle_ended:
            # Player Choice Phase
            player_skill = self._wait_for_choice(
                self.player, 
                [SelectThing(skill) for skill in self.player_creature.skills]
            ).thing

            # Bot Choice Phase
            bot_skill = self._wait_for_choice(
                self.bot,
                [SelectThing(skill) for skill in self.bot_creature.skills]
            ).thing

            # Resolution Phase
            first, second = self.determine_order(
                (self.player, self.player_creature, player_skill),
                (self.bot, self.bot_creature, bot_skill)
            )

            # Execute skills in order
            for attacker, creature, skill in [first, second]:
                self.execute_skill(attacker, creature, skill)
                if self.check_battle_end():
                    break

        # Reset creatures and transition
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
        self._transition_to_scene("MainMenuScene")

    def determine_order(self, a, b):
        if a[1].speed > b[1].speed:
            return a, b
        elif b[1].speed > a[1].speed:
            return b, a
        else:
            return (a, b) if random.random() < 0.5 else (b, a)

    def execute_skill(self, attacker, attacker_creature, skill):
        defender = self.bot if attacker == self.player else self.player
        defender_creature = self.bot_creature if attacker == self.player else self.player_creature

        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        factor = self.get_type_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * factor)

        defender_creature.hp = max(0, defender_creature.hp - final_damage)

        self._show_text(attacker, 
            f"{attacker_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender_creature.display_name}")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self.battle_ended = True
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self.battle_ended = True
            return True
        return False

    def get_type_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }

        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
