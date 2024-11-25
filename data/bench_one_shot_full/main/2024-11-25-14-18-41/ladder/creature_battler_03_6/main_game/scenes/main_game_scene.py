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

{self.bot.display_name}'s {self.bot_creature.display_name}
HP: {self.bot_creature.hp}/{self.bot_creature.max_hp}
Type: {self.bot_creature.creature_type}"""

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
                if creature.hp <= 0:
                    continue
                    
                defender = self.bot_creature if attacker == self.player else self.player_creature
                damage = self._calculate_damage(skill, creature, defender)
                defender.hp -= damage

                self._show_text(attacker, f"{creature.display_name} used {skill.display_name}!")
                self._show_text(attacker, f"Dealt {damage} damage!")

                if defender.hp <= 0:
                    winner = "You win!" if attacker == self.player else "You lose!"
                    self._show_text(self.player, winner)
                    self._transition_to_scene("MainMenuScene")
                    return

    def _get_skill_choice(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return next(skill for skill in creature.skills if skill.display_name == choice.display_name)

    def _determine_order(self, p1_data, p2_data):
        p1_speed = p1_data[1].speed
        p2_speed = p2_data[1].speed
        
        if p1_speed > p2_speed:
            return p1_data, p2_data
        elif p2_speed > p1_speed:
            return p2_data, p1_data
        else:
            return random.sample([p1_data, p2_data], 2)

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
