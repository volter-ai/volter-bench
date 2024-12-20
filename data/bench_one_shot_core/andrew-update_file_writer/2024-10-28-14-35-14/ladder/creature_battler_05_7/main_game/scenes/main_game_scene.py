from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.initialize_battle()
        self.queued_actions = {"player": None, "bot": None}

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
            self.player_turn()
            if self.check_battle_end():
                self.end_battle()
                return
            self.bot_turn()
            if self.check_battle_end():
                self.end_battle()
                return
            self.resolve_turn()

    def player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if attack_button == choice:
                skill = self.choose_skill(self.player)
                if skill:
                    self.queued_actions["player"] = ("attack", skill)
                    return
            elif swap_button == choice:
                creature = self.choose_creature(self.player)
                if creature:
                    self.queued_actions["player"] = ("swap", creature)
                    return

    def bot_turn(self):
        bot_choice = random.choice(["attack", "swap"])
        if bot_choice == "attack":
            skill = random.choice(self.bot.active_creature.skills)
            self.queued_actions["bot"] = ("attack", skill)
        else:
            available_creatures = [c for c in self.bot.creatures if c != self.bot.active_creature and c.hp > 0]
            if available_creatures:
                creature = random.choice(available_creatures)
                self.queued_actions["bot"] = ("swap", creature)
            else:
                skill = random.choice(self.bot.active_creature.skills)
                self.queued_actions["bot"] = ("attack", skill)

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

    def resolve_turn(self):
        player_action, player_target = self.queued_actions["player"]
        bot_action, bot_target = self.queued_actions["bot"]

        # Handle swaps first
        if player_action == "swap":
            self.player.active_creature = player_target
            self._show_text(self.player, f"{self.player.display_name} swapped to {player_target.display_name}!")

        if bot_action == "swap":
            self.bot.active_creature = bot_target
            self._show_text(self.player, f"{self.bot.display_name} swapped to {bot_target.display_name}!")

        # Determine order of attacks based on speed
        if player_action == "attack" and bot_action == "attack":
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                self.execute_attack(self.player, self.bot, player_target)
                if self.bot.active_creature.hp > 0:
                    self.execute_attack(self.bot, self.player, bot_target)
            elif self.player.active_creature.speed < self.bot.active_creature.speed:
                self.execute_attack(self.bot, self.player, bot_target)
                if self.player.active_creature.hp > 0:
                    self.execute_attack(self.player, self.bot, player_target)
            else:
                if random.choice([True, False]):
                    self.execute_attack(self.player, self.bot, player_target)
                    if self.bot.active_creature.hp > 0:
                        self.execute_attack(self.bot, self.player, bot_target)
                else:
                    self.execute_attack(self.bot, self.player, bot_target)
                    if self.player.active_creature.hp > 0:
                        self.execute_attack(self.player, self.bot, player_target)
        elif player_action == "attack":
            self.execute_attack(self.player, self.bot, player_target)
        elif bot_action == "attack":
            self.execute_attack(self.bot, self.player, bot_target)

        self.queued_actions = {"player": None, "bot": None}

    def execute_attack(self, attacker, defender, skill):
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender.active_creature.display_name}!")
        
        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} fainted!")
            self.force_swap(defender)

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = float(attacker.attack + skill.base_damage - defender.defense)
        else:
            raw_damage = float(attacker.sp_attack * skill.base_damage / defender.sp_defense)

        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * effectiveness)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_effectiveness(self, attack_type, defend_type):
        effectiveness_chart = {
            "normal": {"normal": 1.0, "fire": 1.0, "water": 1.0, "leaf": 1.0},
            "fire": {"normal": 1.0, "fire": 0.5, "water": 0.5, "leaf": 2.0},
            "water": {"normal": 1.0, "fire": 2.0, "water": 0.5, "leaf": 0.5},
            "leaf": {"normal": 1.0, "fire": 0.5, "water": 2.0, "leaf": 0.5}
        }
        return effectiveness_chart[attack_type][defend_type]

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            if player == self.player:
                new_creature = self.choose_creature(player)
                if new_creature:
                    player.active_creature = new_creature
                    self._show_text(self.player, f"{player.display_name} sent out {new_creature.display_name}!")
                else:
                    self._show_text(self.player, f"{player.display_name} has no more creatures able to battle!")
            else:
                new_creature = random.choice(available_creatures)
                player.active_creature = new_creature
                self._show_text(self.player, f"{player.display_name} sent out {new_creature.display_name}!")
        else:
            self._show_text(self.player, f"{player.display_name} has no more creatures able to battle!")

    def check_battle_end(self):
        if all(creature.hp <= 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        if all(creature.hp <= 0 for creature in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def end_battle(self):
        self.reset_creatures()
        play_again_button = Button("Play Again")
        quit_button = Button("Quit")
        choices = [play_again_button, quit_button]
        choice = self._wait_for_choice(self.player, choices)

        if play_again_button == choice:
            self._transition_to_scene("MainMenuScene")
        else:
            self._quit_whole_game()

    def reset_creatures(self):
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp
