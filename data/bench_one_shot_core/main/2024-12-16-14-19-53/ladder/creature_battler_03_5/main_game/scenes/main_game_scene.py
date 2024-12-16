from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_skills = {}

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        self._show_text(self.bot, "Battle Start!")

        while True:
            # Player Choice Phase
            self.player_choice_phase()
            
            # Bot Choice Phase  
            self.bot_choice_phase()

            # Resolution Phase
            self.resolution_phase()

            # Check for battle end
            if self.check_battle_end():
                # Instead of just breaking, properly end the game
                self._quit_whole_game()

    def player_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.queued_skills[self.player.uid] = choice.thing

    def bot_choice_phase(self):
        choices = [SelectThing(skill) for skill in self.bot_creature.skills]
        choice = self._wait_for_choice(self.bot, choices)
        self.queued_skills[self.bot.uid] = choice.thing

    def resolution_phase(self):
        # Determine order based on speed
        first = self.player
        second = self.bot
        if self.bot_creature.speed > self.player_creature.speed:
            first, second = second, first
        elif self.bot_creature.speed == self.player_creature.speed:
            if random.random() < 0.5:
                first, second = second, first

        # Execute skills in order
        for attacker in [first, second]:
            defender = self.bot if attacker == self.player else self.player
            self.execute_skill(attacker, defender)

    def execute_skill(self, attacker, defender):
        skill = self.queued_skills[attacker.uid]
        attacker_creature = self.player_creature if attacker == self.player else self.bot_creature
        defender_creature = self.bot_creature if attacker == self.player else self.player_creature

        # Calculate raw damage
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense

        # Apply type effectiveness
        factor = self.get_type_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * factor)
        
        # Apply damage
        defender_creature.hp = max(0, defender_creature.hp - final_damage)

        # Show result
        message = f"{attacker_creature.display_name} used {skill.display_name} for {final_damage} damage!"
        self._show_text(self.player, message)
        self._show_text(self.bot, message)

    def get_type_factor(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }

        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
            self._show_text(self.bot, "You won!")
            return True
        elif self.bot_creature.hp <= 0:
            self._show_text(self.player, "You won!")
            self._show_text(self.bot, "You lost!")
            return True
        return False
