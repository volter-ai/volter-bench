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
{self.player.display_name}'s {self.player_creature.display_name}:
HP: {self.player_creature.hp}/{self.player_creature.max_hp}
Type: {self.player_creature.creature_type}

{self.bot.display_name}'s {self.bot_creature.display_name}:
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

            # Player turn
            player_skill = self._get_skill_choice(self.player, self.player_creature)
            bot_skill = self._get_skill_choice(self.bot, self.bot_creature)

            # Determine order
            first, second = self._determine_turn_order(
                (self.player, self.player_creature, player_skill),
                (self.bot, self.bot_creature, bot_skill)
            )

            # Execute turns
            for attacker, creature, skill in [first, second]:
                defender_creature = self.bot_creature if attacker == self.player else self.player_creature
                damage = self._calculate_damage(skill, creature, defender_creature)
                defender_creature.hp -= damage
                
                self._show_text(self.player, f"{creature.display_name} used {skill.display_name} for {damage} damage!")
                self._show_text(self.bot, f"{creature.display_name} used {skill.display_name} for {damage} damage!")

                if defender_creature.hp <= 0:
                    winner = self.player if defender_creature == self.bot_creature else self.bot
                    self._show_text(self.player, f"{winner.display_name} wins!")
                    self._show_text(self.bot, f"{winner.display_name} wins!")
                    self._transition_to_scene("MainMenuScene")
                    return

    def _get_skill_choice(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _determine_turn_order(self, player_data, bot_data):
        if player_data[1].speed > bot_data[1].speed:
            return player_data, bot_data
        elif player_data[1].speed < bot_data[1].speed:
            return bot_data, player_data
        else:
            return random.choice([(player_data, bot_data), (bot_data, player_data)])

    def _calculate_damage(self, skill, attacker, defender):
        # Calculate base damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense

        # Calculate type multiplier
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
