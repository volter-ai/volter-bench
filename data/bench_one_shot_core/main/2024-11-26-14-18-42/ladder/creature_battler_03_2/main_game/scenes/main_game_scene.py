from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.phase = "player_choice"
        self.player_creature = player.creatures[0]
        self.bot_creature = self.bot.creatures[0]
        self.queued_player_skill = None
        self.queued_bot_skill = None

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.bot.display_name}'s {self.bot_creature.display_name}: HP {self.bot_creature.hp}/{self.bot_creature.max_hp}

Phase: {self.phase}
"""

    def run(self):
        while True:
            # Player choice phase
            self.phase = "player_choice"
            choices = [SelectThing(skill) for skill in self.player_creature.skills]
            self.queued_player_skill = self._wait_for_choice(self.player, choices).thing

            # Bot choice phase  
            self.phase = "bot_choice"
            choices = [SelectThing(skill) for skill in self.bot_creature.skills]
            self.queued_bot_skill = self._wait_for_choice(self.bot, choices).thing

            # Resolution phase
            self.phase = "resolution"
            self.resolve_turn()

            # Check win condition
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                self._quit_whole_game()  # End game instead of break
            elif self.bot_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                self._quit_whole_game()  # End game instead of break

    def resolve_turn(self):
        first = self.player
        second = self.bot
        first_skill = self.queued_player_skill
        second_skill = self.queued_bot_skill
        
        # Speed check
        if self.bot_creature.speed > self.player_creature.speed or \
           (self.bot_creature.speed == self.player_creature.speed and random.random() < 0.5):
            first, second = second, first
            first_skill, second_skill = second_skill, first_skill

        # Execute skills
        self.execute_skill(first_skill, 
                          self.player_creature if first == self.player else self.bot_creature,
                          self.bot_creature if first == self.player else self.player_creature)
        
        if second_skill and (self.player_creature.hp > 0 and self.bot_creature.hp > 0):
            self.execute_skill(second_skill,
                             self.player_creature if second == self.player else self.bot_creature,
                             self.bot_creature if second == self.player else self.player_creature)

    def execute_skill(self, skill, attacker, defender):
        # Calculate raw damage
        raw_damage = attacker.attack + skill.base_damage - defender.defense

        # Get type effectiveness
        factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        # Calculate final damage
        final_damage = int(factor * raw_damage)
        defender.hp = max(0, defender.hp - final_damage)

        # Show result
        effectiveness = "It's super effective!" if factor > 1 else "It's not very effective..." if factor < 1 else ""
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! {effectiveness}")

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)
