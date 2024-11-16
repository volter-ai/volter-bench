from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]

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
{' '.join([f'> {skill.display_name}' for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Show battle state
            self._show_text(self.player, str(self))
            self._show_text(self.bot, str(self))

            # Player and bot choose skills
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            bot_skill = self._get_skill_choice(self.bot, self.bot_creature)

            # Determine order and resolve
            first, second = self._determine_order(
                (self.player, self.player_creature, player_skill),
                (self.bot, self.bot_creature, bot_skill)
            )

            # Execute turns
            self._execute_turn(*first)
            if self._check_battle_end():
                break

            self._execute_turn(*second) 
            if self._check_battle_end():
                break

    def _get_skill_choice(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(s for s in creature.skills if s.display_name == choice.display_name)

    def _determine_order(self, a, b):
        if a[1].speed > b[1].speed:
            return a, b
        elif b[1].speed > a[1].speed:
            return b, a
        else:
            return random.choice([(a, b), (b, a)])

    def _calculate_damage(self, attacker, skill, defender):
        # Base damage calculation
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Type multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf":
                multiplier = 2.0
            elif defender.creature_type == "water":
                multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire":
                multiplier = 2.0
            elif defender.creature_type == "leaf":
                multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water":
                multiplier = 2.0
            elif defender.creature_type == "fire":
                multiplier = 0.5

        return int(raw_damage * multiplier)

    def _execute_turn(self, attacker, attacker_creature, skill):
        defender = self.bot if attacker == self.player else self.player
        defender_creature = self.bot_creature if attacker == self.player else self.player_creature

        damage = self._calculate_damage(attacker_creature, skill, defender_creature)
        defender_creature.hp = max(0, defender_creature.hp - damage)

        self._show_text(self.player, 
            f"{attacker_creature.display_name} used {skill.display_name} for {damage} damage!")
        self._show_text(self.bot,
            f"{attacker_creature.display_name} used {skill.display_name} for {damage} damage!")

    def _check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._show_text(self.bot, "You won!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._show_text(self.bot, "You lost!")
            self._transition_to_scene("MainMenuScene") 
            return True
        return False
