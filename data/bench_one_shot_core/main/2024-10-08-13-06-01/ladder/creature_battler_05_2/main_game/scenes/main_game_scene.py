from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random
import time


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
            self.player_choice_phase(self.player)
            self.player_choice_phase(self.bot)
            self.resolution_phase()

            if self.check_battle_end():
                time.sleep(2)  # Give the player time to see the final result
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene")
                break

    def player_choice_phase(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if choice == attack_button:
                skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
                skill_choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(current_player, skill_choices)
                if isinstance(skill_choice, SelectThing):
                    current_player.chosen_action = ("attack", skill_choice.thing)
                    break
                else:
                    continue  # This is the "Back" button, so we continue the loop
            elif choice == swap_button:
                swap_choices = [SelectThing(creature) for creature in current_player.creatures if creature != current_player.active_creature and creature.hp > 0]
                swap_choices.append(Button("Back"))
                swap_choice = self._wait_for_choice(current_player, swap_choices)
                if isinstance(swap_choice, SelectThing):
                    current_player.chosen_action = ("swap", swap_choice.thing)
                    break
                else:
                    continue  # This is the "Back" button, so we continue the loop

    def resolution_phase(self):
        players = [self.player, self.bot]
        random.shuffle(players)
        players.sort(key=lambda p: p.active_creature.speed, reverse=True)

        for player in players:
            opponent = self.bot if player == self.player else self.player
            action, target = player.chosen_action

            if action == "swap":
                player.active_creature = target
                self._show_text(player, f"{player.display_name} swapped to {target.display_name}!")
            elif action == "attack":
                skill = target
                damage = self.calculate_damage(player.active_creature, opponent.active_creature, skill)
                opponent.active_creature.hp = max(0, opponent.active_creature.hp - damage)
                self._show_text(player, f"{player.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

            if opponent.active_creature.hp == 0:
                self._show_text(opponent, f"{opponent.active_creature.display_name} fainted!")
                self.force_swap(opponent)

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)

    def get_type_effectiveness(self, skill_type: str, defender_type: str) -> float:
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def force_swap(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not available_creatures:
            return

        swap_choices = [SelectThing(creature) for creature in available_creatures]
        swap_choice = self._wait_for_choice(player, swap_choices)
        player.active_creature = swap_choice.thing
        self._show_text(player, f"{player.display_name} swapped to {player.active_creature.display_name}!")

    def check_battle_end(self) -> bool:
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(c.hp == 0 for c in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures(self):
        for player in [self.player, self.bot]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
