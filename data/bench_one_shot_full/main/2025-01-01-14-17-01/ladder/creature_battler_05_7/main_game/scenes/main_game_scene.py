from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player_action = None
        self.bot_action = None

    def __str__(self):
        return f"""===Main Game===
Player: {self.player.display_name}
Active Creature: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})

Bot: {self.bot.display_name}
Active Creature: {self.bot.active_creature.display_name} (HP: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp})
"""

    def run(self):
        while self.player.active_creature.hp > 0 and self.bot.active_creature.hp > 0:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()
            self.check_forced_swapping()

    def player_choice_phase(self):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choices = [attack_button, swap_button]
        choice = self._wait_for_choice(self.player, choices)

        if choice == attack_button:
            self.player_action = self.attack_phase(self.player)
        elif choice == swap_button:
            self.player_action = self.swap_phase(self.player)

    def foe_choice_phase(self):
        # Randomly choose attack or swap for the bot
        if random.choice([True, False]):
            self.bot_action = self.attack_phase(self.bot)
        else:
            self.bot_action = self.swap_phase(self.bot)

    def resolution_phase(self):
        # Resolve actions, calculate damage, and apply it
        if isinstance(self.player_action, Skill) and isinstance(self.bot_action, Skill):
            # Determine order based on speed
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                self.execute_skill(self.player, self.bot, self.player_action)
                if self.bot.active_creature.hp > 0:
                    self.execute_skill(self.bot, self.player, self.bot_action)
            else:
                self.execute_skill(self.bot, self.player, self.bot_action)
                if self.player.active_creature.hp > 0:
                    self.execute_skill(self.player, self.bot, self.player_action)
        elif isinstance(self.player_action, Creature):
            # Player swapped, bot attacks
            self.execute_skill(self.bot, self.player, self.bot_action)
        elif isinstance(self.bot_action, Creature):
            # Bot swapped, player attacks
            self.execute_skill(self.player, self.bot, self.player_action)

    def attack_phase(self, player: Player):
        # Logic for attack phase
        active_creature = player.active_creature
        skill_choices = [SelectThing(skill) for skill in active_creature.skills]
        chosen_skill = self._wait_for_choice(player, skill_choices).thing
        return chosen_skill

    def swap_phase(self, player: Player):
        # Logic for swap phase
        available_creatures = [creature for creature in player.creatures if creature.hp > 0 and creature != player.active_creature]
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        chosen_creature = self._wait_for_choice(player, creature_choices).thing
        player.active_creature = chosen_creature
        return chosen_creature

    def check_forced_swapping(self):
        # Check if any active creature is knocked out and force swap
        for player in [self.player, self.bot]:
            if player.active_creature.hp <= 0:
                self.swap_phase(player)

    def execute_skill(self, attacker: Player, defender: Player, skill: Skill):
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp -= damage
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Calculate weakness-resistance factor
        factor = self.get_weakness_resistance_factor(skill.skill_type, defender.creature_type)

        # Calculate final damage
        final_damage = int(factor * raw_damage)
        return max(0, final_damage)

    def get_weakness_resistance_factor(self, skill_type: str, creature_type: str) -> float:
        # Define type relationships
        type_chart = {
            "normal": {},
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return type_chart.get(skill_type, {}).get(creature_type, 1)
