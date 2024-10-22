import random

from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        self.player_action = None
        self.bot_action = None

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
{self.bot.display_name}: {self.bot.active_creature.display_name} (HP: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp})

> Attack
> Swap (if available)
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
        self.reset_creatures_state()

    def player_turn(self):
        while True:
            attack_button = Button("Attack")
            choices = [attack_button]

            available_creatures = [c for c in self.player.creatures if c != self.player.active_creature and c.hp > 0]
            if available_creatures:
                swap_button = Button("Swap")
                choices.append(swap_button)

            choice = self._wait_for_choice(self.player, choices)

            if attack_button == choice:
                skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                skill_choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                if skill_choice == Button("Back"):
                    continue
                self.player_action = ("attack", skill_choice.thing)
                break
            elif swap_button == choice:
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choices.append(Button("Back"))
                creature_choice = self._wait_for_choice(self.player, creature_choices)
                if creature_choice == Button("Back"):
                    continue
                self.player_action = ("swap", creature_choice.thing)
                break

    def bot_turn(self):
        while True:
            if random.choice([True, False]):  # 50% chance to attempt attack
                skill = random.choice(self.bot.active_creature.skills)
                self.bot_action = ("attack", skill)
                break
            else:
                available_creatures = [c for c in self.bot.creatures if c != self.bot.active_creature and c.hp > 0]
                if available_creatures:
                    creature = random.choice(available_creatures)
                    self.bot_action = ("swap", creature)
                    break
                # If no creatures available to swap, continue the loop to force an attack

    def resolve_turn(self):
        actions = [
            (self.player, self.player_action),
            (self.bot, self.bot_action)
        ]
        
        # Sort actions based on speed or swap priority
        actions.sort(key=lambda x: (x[1][0] != "swap", -x[0].active_creature.speed, random.random()))

        for actor, action in actions:
            if action[0] == "swap":
                self.perform_swap(actor, action[1])
            else:
                self.perform_attack(actor, action[1])

        self.check_and_force_swap(self.player)
        self.check_and_force_swap(self.bot)

    def perform_swap(self, actor, new_creature):
        actor.active_creature = new_creature
        self._show_text(self.player, f"{actor.display_name} swapped to {new_creature.display_name}!")

    def perform_attack(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender.active_creature.display_name}!")

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_effectiveness(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def check_and_force_swap(self, player):
        if player.active_creature.hp == 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if available_creatures:
                if player == self.player:
                    creature_choices = [SelectThing(creature) for creature in available_creatures]
                    creature_choice = self._wait_for_choice(player, creature_choices)
                    new_creature = creature_choice.thing
                else:
                    new_creature = random.choice(available_creatures)
                self.perform_swap(player, new_creature)
            else:
                self._show_text(self.player, f"{player.display_name} has no more creatures available!")

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif all(creature.hp == 0 for creature in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def reset_creatures_state(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
