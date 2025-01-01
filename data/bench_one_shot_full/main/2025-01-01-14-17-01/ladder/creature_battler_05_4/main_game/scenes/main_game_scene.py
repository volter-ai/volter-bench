from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    TYPE_EFFECTIVENESS = {
        "normal": {},
        "fire": {"leaf": 2, "water": 0.5},
        "water": {"fire": 2, "leaf": 0.5},
        "leaf": {"water": 2, "fire": 0.5}
    }

    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.action_queue = []

    def __str__(self):
        return f"""===Main Game===
Player: {self.player.display_name}
Active Creature: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})

Bot: {self.bot.display_name}
Active Creature: {self.bot.active_creature.display_name} (HP: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp})

Choose your action:
1: Attack
2: Swap
"""

    def run(self):
        while self.player.active_creature.hp > 0 and self.bot.active_creature.hp > 0:
            self.player_turn()
            if self.bot.active_creature.hp > 0:
                self.bot_turn()
            self.resolve_turn()
            self.check_forced_swap()

    def player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            back_button = Button("Back")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if choice == attack_button:
                if self.player_attack():
                    break
            elif choice == swap_button:
                if self.player_swap():
                    break

    def player_attack(self):
        skills = self.player.active_creature.skills
        skill_choices = [SelectThing(skill) for skill in skills]
        skill_choices.append(Button("Back"))
        chosen_skill = self._wait_for_choice(self.player, skill_choices)
        if isinstance(chosen_skill, Button) and chosen_skill.display_name == "Back":
            return False
        self.action_queue.append((self.player.active_creature, chosen_skill.thing))
        return True

    def player_swap(self):
        creatures = [creature for creature in self.player.creatures if creature.hp > 0 and creature != self.player.active_creature]
        creature_choices = [SelectThing(creature) for creature in creatures]
        creature_choices.append(Button("Back"))
        chosen_creature = self._wait_for_choice(self.player, creature_choices)
        if isinstance(chosen_creature, Button) and chosen_creature.display_name == "Back":
            return False
        self.player.active_creature = chosen_creature.thing
        return True

    def bot_turn(self):
        if random.choice([True, False]):
            self.bot_attack()
        else:
            self.bot_swap()

    def bot_attack(self):
        skill = random.choice(self.bot.active_creature.skills)
        self.action_queue.append((self.bot.active_creature, skill))

    def bot_swap(self):
        creatures = [creature for creature in self.bot.creatures if creature.hp > 0 and creature != self.bot.active_creature]
        if creatures:
            self.bot.active_creature = random.choice(creatures)

    def resolve_turn(self):
        self.action_queue.sort(key=lambda x: x[0].speed, reverse=True)
        for creature, skill in self.action_queue:
            if creature.hp > 0:
                self.execute_skill(creature, skill)
        self.action_queue.clear()

    def execute_skill(self, attacker, skill):
        defender = self.bot.active_creature if attacker == self.player.active_creature else self.player.active_creature
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        effectiveness = self.TYPE_EFFECTIVENESS.get(skill.skill_type, {}).get(defender.creature_type, 1)
        final_damage = int(raw_damage * effectiveness)
        defender.hp = max(defender.hp - final_damage, 0)

    def check_forced_swap(self):
        if self.player.active_creature.hp == 0:
            self.force_swap(self.player)
        if self.bot.active_creature.hp == 0:
            self.force_swap(self.bot)

    def force_swap(self, player):
        creatures = [creature for creature in player.creatures if creature.hp > 0]
        if creatures:
            player.active_creature = random.choice(creatures)
        else:
            self.end_battle(player)

    def end_battle(self, loser):
        winner = self.player if loser == self.bot else self.bot
        self._show_text(self.player, f"{winner.display_name} wins the battle!")
        self._quit_whole_game()
