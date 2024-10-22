from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.bot.display_name}: {self.bot_creature.display_name} (HP: {self.bot_creature.hp}/{self.bot_creature.max_hp})

Player's turn:
> {self.player_creature.skills[0].display_name}
> {self.player_creature.skills[1].display_name}
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.bot_creature.display_name} appeared!")
        self.battle_loop()

    def battle_loop(self):
        while True:
            player_skill = self.player_turn()
            bot_skill = self.bot_turn()
            self.resolve_turn(player_skill, bot_skill)

            if self.check_battle_end():
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def bot_turn(self):
        choices = [SelectThing(skill) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        return choice.thing

    def resolve_turn(self, player_skill, bot_skill):
        first, second = self.determine_turn_order(player_skill, bot_skill)
        self.execute_skill(*first)
        if not self.check_battle_end():
            self.execute_skill(*second)

    def determine_turn_order(self, player_skill, bot_skill):
        if self.player_creature.speed > self.bot_creature.speed:
            return (self.player, self.player_creature, player_skill, self.bot_creature), (self.bot, self.bot_creature, bot_skill, self.player_creature)
        elif self.player_creature.speed < self.bot_creature.speed:
            return (self.bot, self.bot_creature, bot_skill, self.player_creature), (self.player, self.player_creature, player_skill, self.bot_creature)
        else:
            if random.random() < 0.5:
                return (self.player, self.player_creature, player_skill, self.bot_creature), (self.bot, self.bot_creature, bot_skill, self.player_creature)
            else:
                return (self.bot, self.bot_creature, bot_skill, self.player_creature), (self.player, self.player_creature, player_skill, self.bot_creature)

    def execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        damage = self.calculate_damage(attacker_creature, skill, defender_creature)
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender_creature.display_name} took {damage} damage!")

    def calculate_damage(self, attacker, skill, defender):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            # Corrected calculation for special skills using division
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)

    def get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5},
            "normal": {}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player_creature.display_name} fainted! You lost the battle.")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, f"{self.bot_creature.display_name} fainted! You won the battle!")
            return True
        return False

    def reset_creatures(self):
        self.player_creature.hp = self.player_creature.max_hp
        self.bot_creature.hp = self.bot_creature.max_hp
