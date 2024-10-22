from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
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
            if not self.player_turn():
                break
            if self.check_battle_end():
                break
            if not self.bot_turn():
                break
            if self.check_battle_end():
                break

    def player_turn(self):
        self._show_text(self.player, f"It's your turn, {self.player.display_name}!")
        action = self.get_player_action(self.player)
        if action is None:
            return False
        self.execute_action(self.player, self.bot, action)
        return True

    def bot_turn(self):
        self._show_text(self.player, f"It's {self.bot.display_name}'s turn!")
        action = self.get_player_action(self.bot)
        if action is None:
            return False
        self.execute_action(self.bot, self.player, action)
        return True

    def get_player_action(self, acting_player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choices = [attack_button, swap_button]
        choice = self._wait_for_choice(acting_player, choices)

        if attack_button == choice:
            return self.get_attack_action(acting_player)
        elif swap_button == choice:
            swap_action = self.get_swap_action(acting_player)
            if swap_action is None:
                self._show_text(acting_player, "No creatures available to swap!")
                return self.get_attack_action(acting_player)
            return swap_action

    def get_attack_action(self, acting_player):
        skill_choices = [SelectThing(skill) for skill in acting_player.active_creature.skills]
        return self._wait_for_choice(acting_player, skill_choices)

    def get_swap_action(self, acting_player):
        available_creatures = [creature for creature in acting_player.creatures if creature != acting_player.active_creature and creature.hp > 0]
        if not available_creatures:
            return None
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        return self._wait_for_choice(acting_player, creature_choices)

    def execute_action(self, acting_player, defending_player, action):
        if isinstance(action.thing, Skill):
            self.execute_attack(acting_player, defending_player, action.thing)
        elif isinstance(action.thing, Creature):
            self.execute_swap(acting_player, action.thing)

    def execute_attack(self, attacker, defender, skill):
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender.active_creature.display_name}!")

    def execute_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, f"All your creatures have been defeated. {self.bot.display_name} wins!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif all(creature.hp == 0 for creature in self.bot.creatures):
            self._show_text(self.player, f"All opponent's creatures have been defeated. You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False

    def force_swap(self, player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if not available_creatures:
            return False
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        new_creature = self._wait_for_choice(player, creature_choices).thing
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")
        return True
