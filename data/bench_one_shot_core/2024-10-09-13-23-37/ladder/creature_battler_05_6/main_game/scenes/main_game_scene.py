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
                skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                skill_choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                if skill_choice == Button("Back"):
                    continue
                self.player_action = ("attack", skill_choice.thing)
                break
            elif choice == swap_button:
                valid_swap_creatures = [c for c in self.player.creatures if c != self.player.active_creature and c.hp > 0]
                if not valid_swap_creatures:
                    self._show_text(self.player, "No valid creatures to swap to!")
                    continue
                creature_choices = [SelectThing(creature) for creature in valid_swap_creatures]
                creature_choices.append(Button("Back"))
                creature_choice = self._wait_for_choice(self.player, creature_choices)
                if creature_choice == Button("Back"):
                    continue
                self.player_action = ("swap", creature_choice.thing)
                break

    def bot_turn(self):
        available_creatures = [c for c in self.bot.creatures if c != self.bot.active_creature and c.hp > 0]
        
        if available_creatures and random.choice([True, False]):  # 50% chance to swap if possible
            creature = random.choice(available_creatures)
            self.bot_action = ("swap", creature)
        else:
            skill = random.choice(self.bot.active_creature.skills)
            self.bot_action = ("attack", skill)

    def resolve_turn(self):
        actions = [
            (self.player, self.player_action),
            (self.bot, self.bot_action)
        ]
        
        # Sort actions based on speed or swap priority, with random tiebreaker
        actions.sort(key=lambda x: (x[1][0] != "swap", -x[0].active_creature.speed, random.random()))

        for actor, action in actions:
            if action[0] == "swap":
                self.perform_swap(actor, action[1])
            else:
                self.perform_attack(actor, action[1])

            # Check if forced swap is needed after each action
            self.check_forced_swap(self.player)
            self.check_forced_swap(self.bot)

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
            raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        else:
            raw_damage = float(attacker.sp_attack) / float(defender.sp_defense) * float(skill.base_damage)

        type_effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_effectiveness(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1.0)

    def check_forced_swap(self, player):
        if player.active_creature.hp == 0:
            valid_swap_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
            if valid_swap_creatures:
                if player == self.player:
                    self._show_text(self.player, f"{player.active_creature.display_name} has fainted! Choose a new creature.")
                    creature_choices = [SelectThing(creature) for creature in valid_swap_creatures]
                    creature_choice = self._wait_for_choice(player, creature_choices)
                    self.perform_swap(player, creature_choice.thing)
                else:
                    new_creature = random.choice(valid_swap_creatures)
                    self.perform_swap(player, new_creature)

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
