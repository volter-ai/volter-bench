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
{', '.join(skill.display_name for skill in self.player_creature.skills)}
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
            for attacker, creature, skill in [first, second]:
                if self._execute_skill(attacker, creature, skill):
                    return

    def _get_skill_choice(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _determine_order(self, player_data, bot_data):
        if player_data[1].speed > bot_data[1].speed:
            return player_data, bot_data
        elif player_data[1].speed < bot_data[1].speed:
            return bot_data, player_data
        else:
            return random.sample([player_data, bot_data], 2)

    def _calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
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

    def _execute_skill(self, attacker, attacker_creature, skill):
        if attacker == self.player:
            defender_creature = self.bot_creature
            defender = self.bot
        else:
            defender_creature = self.player_creature
            defender = self.player

        damage = self._calculate_damage(skill, attacker_creature, defender_creature)
        defender_creature.hp -= damage

        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"Dealt {damage} damage!")

        if defender_creature.hp <= 0:
            defender_creature.hp = 0
            winner = "You" if attacker == self.player else "Bot"
            self._show_text(self.player, f"{winner} won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True

        return False
