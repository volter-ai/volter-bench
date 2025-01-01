from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.initial_player_creatures = [(creature.prototype_id, creature.hp) for creature in player.creatures]

    def __str__(self):
        return f"""===Main Game===
Player: {self.player.display_name}
Active Creature: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})

Bot: {self.bot.display_name}
Active Creature: {self.bot.active_creature.display_name} (HP: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp})
"""

    def run(self):
        try:
            while self.player.active_creature.hp > 0 and self.bot.active_creature.hp > 0:
                player_action = self.player_choice_phase()
                bot_action = self.foe_choice_phase()
                self.resolution_phase(player_action, bot_action)
        finally:
            self.reset_creatures_state()

        self.end_game()

    def player_choice_phase(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if attack_button == choice:
                skill_action = self.attack_phase(self.player)
                if skill_action:
                    return skill_action
            elif swap_button == choice:
                swap_action = self.swap_phase(self.player)
                if swap_action:
                    return swap_action

    def foe_choice_phase(self):
        # Randomly choose between attack and swap for the bot
        if random.choice([True, False]):
            return self.attack_phase(self.bot)
        else:
            return self.swap_phase(self.bot)

    def resolution_phase(self, player_action, bot_action):
        # Resolve actions based on speed or swap priority
        if player_action['type'] == 'swap':
            self.player.active_creature = player_action['creature']
        if bot_action['type'] == 'swap':
            self.bot.active_creature = bot_action['creature']

        if player_action['type'] == 'attack' and bot_action['type'] == 'attack':
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                self.execute_attack(player_action['skill'], self.player.active_creature, self.bot.active_creature)
                if self.bot.active_creature.hp > 0:
                    self.execute_attack(bot_action['skill'], self.bot.active_creature, self.player.active_creature)
            else:
                self.execute_attack(bot_action['skill'], self.bot.active_creature, self.player.active_creature)
                if self.player.active_creature.hp > 0:
                    self.execute_attack(player_action['skill'], self.player.active_creature, self.bot.active_creature)

    def attack_phase(self, player: Player):
        skills = player.active_creature.skills
        back_button = Button("Back")
        skill_choices = [SelectThing(skill) for skill in skills] + [back_button]
        skill_choice = self._wait_for_choice(player, skill_choices)
        if skill_choice == back_button:
            return None
        return {'type': 'attack', 'skill': skill_choice.thing}

    def swap_phase(self, player: Player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0 and creature != player.active_creature]
        back_button = Button("Back")
        creature_choices = [SelectThing(creature) for creature in available_creatures] + [back_button]
        creature_choice = self._wait_for_choice(player, creature_choices)
        if creature_choice == back_button:
            return None
        return {'type': 'swap', 'creature': creature_choice.thing}

    def execute_attack(self, skill: Skill, attacker: Creature, defender: Creature):
        # Calculate damage based on skill type and creature stats
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = self.calculate_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * effectiveness)
        defender.hp = max(defender.hp - final_damage, 0)

    def calculate_effectiveness(self, skill_type: str, creature_type: str) -> float:
        effectiveness_chart = {
            "normal": {},
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1)

    def reset_creatures_state(self):
        for creature_id, initial_hp in self.initial_player_creatures:
            creature = next(c for c in self.player.creatures if c.prototype_id == creature_id)
            creature.hp = initial_hp

    def end_game(self):
        if self.player.active_creature.hp <= 0:
            self._show_text(self.player, "You lost!")
        else:
            self._show_text(self.player, "You won!")
        self._quit_whole_game()
