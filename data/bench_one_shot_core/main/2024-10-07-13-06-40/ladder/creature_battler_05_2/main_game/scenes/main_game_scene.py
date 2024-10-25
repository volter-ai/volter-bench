from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

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
            self.resolve_turn()

    def player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if choice == attack_button:
                skill_choice = self.choose_skill()
                if skill_choice:
                    self.player_action = ("attack", skill_choice)
                    break
            elif choice == swap_button:
                creature_choice = self.choose_creature()
                if creature_choice:
                    self.player_action = ("swap", creature_choice)
                    break

    def choose_skill(self):
        while True:
            skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
            back_button = Button("Back")
            choices = skill_choices + [back_button]
            choice = self._wait_for_choice(self.player, choices)

            if choice == back_button:
                return None
            else:
                return choice.thing

    def choose_creature(self):
        while True:
            creature_choices = [SelectThing(creature) for creature in self.player.creatures if creature != self.player.active_creature and creature.hp > 0]
            back_button = Button("Back")
            choices = creature_choices + [back_button]

            if not creature_choices:
                self._show_text(self.player, "No other creatures available to swap!")
                return None

            choice = self._wait_for_choice(self.player, choices)

            if choice == back_button:
                return None
            else:
                return choice.thing

    def bot_turn(self):
        if random.random() < 0.2 and len([c for c in self.bot.creatures if c != self.bot.active_creature and c.hp > 0]) > 0:
            new_creature = random.choice([c for c in self.bot.creatures if c != self.bot.active_creature and c.hp > 0])
            self.bot_action = ("swap", new_creature)
        else:
            skill = random.choice(self.bot.active_creature.skills)
            self.bot_action = ("attack", skill)

    def resolve_turn(self):
        actions = [
            (self.player, self.player_action),
            (self.bot, self.bot_action)
        ]
        
        # Sort actions by speed, and randomize order if speeds are equal
        actions.sort(key=lambda x: (x[0].active_creature.speed, random.random()), reverse=True)

        for player, action in actions:
            if action[0] == "swap":
                player.active_creature = action[1]
                self._show_text(self.player, f"{player.display_name} swapped to {action[1].display_name}!")
            elif action[0] == "attack":
                self.execute_skill(player, action[1])

    def execute_skill(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        type_effectiveness = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * type_effectiveness)

        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} took {final_damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
            self.handle_fainted_creature(defender)

    def get_type_effectiveness(self, skill_type, creature_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, creature_type), 1)

    def handle_fainted_creature(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            if player == self.player:
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                choice = self._wait_for_choice(player, creature_choices)
                player.active_creature = choice.thing
            else:
                player.active_creature = random.choice(available_creatures)
            self._show_text(self.player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        else:
            self._show_text(self.player, f"{player.display_name} has no more creatures left!")

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        elif all(creature.hp == 0 for creature in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            self.reset_creatures()
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creatures(self):
        for player in [self.player, self.bot]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
