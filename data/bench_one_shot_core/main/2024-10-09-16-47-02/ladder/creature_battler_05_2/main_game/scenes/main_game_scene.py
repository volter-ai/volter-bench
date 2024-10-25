from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        self.battle_ended = False

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
{self.bot.display_name}: {self.bot.active_creature.display_name} (HP: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp})

> Attack
> Swap
"""

    def run(self):
        while not self.battle_ended:
            self.player_choice_phase(self.player)
            self.player_choice_phase(self.bot)
            self.resolution_phase()
            
            if self.check_battle_end():
                self.battle_ended = True
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if choice == attack_button:
                skill = self.choose_skill(current_player)
                if skill:
                    current_player.chosen_action = ("attack", skill)
                    break
            elif choice == swap_button:
                new_creature = self.choose_creature(current_player)
                if new_creature:
                    current_player.chosen_action = ("swap", new_creature)
                    break

    def choose_skill(self, player):
        skills = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices = skills + [back_button]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if choice != back_button else None

    def choose_creature(self, player):
        available_creatures = [SelectThing(creature) for creature in player.creatures if creature != player.active_creature and creature.hp > 0]
        back_button = Button("Back")
        choices = available_creatures + [back_button]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if choice != back_button else None

    def resolution_phase(self):
        players = [self.player, self.bot]
        random.shuffle(players)
        # Modified sorting to handle equal speeds randomly
        players.sort(key=lambda p: (p.active_creature.speed, random.random()), reverse=True)

        for player in players:
            opponent = self.bot if player == self.player else self.player
            action, target = player.chosen_action

            if action == "swap":
                player.active_creature = target
                self._show_text(player, f"{player.display_name} swapped to {target.display_name}!")
            elif action == "attack":
                self.execute_skill(player, opponent, target)

    def execute_skill(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender.active_creature.creature_type)
        # Explicitly convert final damage to integer
        final_damage = int(weakness_factor * raw_damage)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)

        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {final_damage} damage!")

    def calculate_weakness_factor(self, skill_type, creature_type):
        weakness_chart = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return weakness_chart.get(skill_type, {}).get(creature_type, 1)

    def check_battle_end(self):
        for player in [self.player, self.bot]:
            if all(creature.hp == 0 for creature in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins the battle!")
                return True
            elif player.active_creature.hp == 0:
                self.force_swap(player)
        return False

    def force_swap(self, player):
        available_creatures = [SelectThing(creature) for creature in player.creatures if creature.hp > 0]
        if available_creatures:
            self._show_text(player, f"{player.active_creature.display_name} fainted! Choose a new creature:")
            choice = self._wait_for_choice(player, available_creatures)
            player.active_creature = choice.thing
            self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")

    def reset_creatures(self):
        for player in [self.player, self.bot]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
