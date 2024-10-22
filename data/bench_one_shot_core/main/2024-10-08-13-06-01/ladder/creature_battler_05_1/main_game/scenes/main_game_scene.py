from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        self.player_action = None
        self.bot_action = None

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
{self.bot.display_name}: {self.bot.active_creature.display_name} (HP: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp})

> Attack
> Swap
"""

    def run(self):
        while True:
            self.player_turn()
            if self.check_battle_end():
                break
            self.bot_turn()
            if self.check_battle_end():
                break
            self.resolution_phase()
            if self.check_battle_end():
                break
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if choice == attack_button:
                skill = self.choose_skill(self.player)
                if skill:
                    self.player_action = ("attack", skill)
                    return
            elif choice == swap_button:
                creature = self.choose_creature(self.player)
                if creature:
                    self.player_action = ("swap", creature)
                    return

    def bot_turn(self):
        if random.random() < 0.2 and len([c for c in self.bot.creatures if c.hp > 0]) > 1:
            available_creatures = [c for c in self.bot.creatures if c != self.bot.active_creature and c.hp > 0]
            self.bot_action = ("swap", random.choice(available_creatures))
        else:
            self.bot_action = ("attack", random.choice(self.bot.active_creature.skills))

    def choose_skill(self, player):
        skills = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices = skills + [back_button]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if choice != back_button else None

    def choose_creature(self, player):
        creatures = [SelectThing(creature) for creature in player.creatures if creature != player.active_creature and creature.hp > 0]
        back_button = Button("Back")
        choices = creatures + [back_button]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if choice != back_button else None

    def resolution_phase(self):
        actions = [
            (self.player, self.player.active_creature, self.player_action),
            (self.bot, self.bot.active_creature, self.bot_action)
        ]

        # Sort actions based on speed, with random tiebreaker for equal speeds
        actions.sort(key=lambda x: (x[2][0] != "swap", -x[1].speed, random.random()))

        for player, creature, action in actions:
            if action[0] == "swap":
                self._show_text(self.player, f"{player.display_name} swaps {creature.display_name} with {action[1].display_name}")
                player.active_creature = action[1]
            elif action[0] == "attack":
                self.execute_skill(player, action[1])

        self.player_action = None
        self.bot_action = None

    def execute_skill(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        defender_creature = defender.active_creature

        self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} uses {skill.display_name}")

        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        type_effectiveness = self.get_type_effectiveness(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * type_effectiveness)

        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} takes {final_damage} damage")

        if defender_creature.hp == 0:
            self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} is knocked out!")
            self.force_swap(defender)

    def get_type_effectiveness(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("water", "fire"): 2,
            ("leaf", "water"): 2,
            ("fire", "water"): 0.5,
            ("water", "leaf"): 0.5,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            self._show_text(self.player, f"{player.display_name} has no more creatures available!")
            return

        if player == self.player:
            self._show_text(self.player, "Choose a creature to swap in:")
            new_creature = self.choose_creature(player)
        else:
            new_creature = random.choice(available_creatures)

        if new_creature is None:
            self._show_text(self.player, f"{player.display_name} has no more creatures available!")
            return

        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} sends out {new_creature.display_name}")

    def check_battle_end(self):
        if all(creature.hp <= 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        if all(creature.hp <= 0 for creature in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
