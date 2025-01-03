from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = self._app.create_bot("basic_opponent")
        self.turn_queue = []

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.opponent.display_name}'s {opponent_creature.display_name}: HP {opponent_creature.hp}/{opponent_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        while True:
            self._player_choice_phase(self.player)
            self._bot_choice_phase(self.opponent)
            self._resolution_phase()
            if self._check_battle_end():
                break
        self._end_battle()

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def _player_choice_phase(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if attack_button == choice:
                skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
                back_button = Button("Back")
                skill_choices.append(back_button)
                skill_choice = self._wait_for_choice(current_player, skill_choices)
                if skill_choice == back_button:
                    continue
                self.turn_queue.append(("attack", current_player, skill_choice.thing))
                break
            elif swap_button == choice:
                available_creatures = [creature for creature in current_player.creatures if creature.hp > 0 and creature != current_player.active_creature]
                if available_creatures:
                    creature_choices = [SelectThing(creature) for creature in available_creatures]
                    back_button = Button("Back")
                    creature_choices.append(back_button)
                    creature_choice = self._wait_for_choice(current_player, creature_choices)
                    if creature_choice == back_button:
                        continue
                    self.turn_queue.append(("swap", current_player, creature_choice.thing))
                    break
                else:
                    self._show_text(current_player, "No other creatures available to swap!")

    def _bot_choice_phase(self, bot_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(bot_player, choices)

            if attack_button == choice:
                skill_choices = [SelectThing(skill) for skill in bot_player.active_creature.skills]
                back_button = Button("Back")
                skill_choices.append(back_button)
                skill_choice = self._wait_for_choice(bot_player, skill_choices)
                if skill_choice == back_button:
                    continue
                self.turn_queue.append(("attack", bot_player, skill_choice.thing))
                break
            elif swap_button == choice:
                available_creatures = [creature for creature in bot_player.creatures if creature.hp > 0 and creature != bot_player.active_creature]
                if available_creatures:
                    creature_choices = [SelectThing(creature) for creature in available_creatures]
                    back_button = Button("Back")
                    creature_choices.append(back_button)
                    creature_choice = self._wait_for_choice(bot_player, creature_choices)
                    if creature_choice == back_button:
                        continue
                    self.turn_queue.append(("swap", bot_player, creature_choice.thing))
                    break
                else:
                    self._show_text(bot_player, "No other creatures available to swap!")

    def _resolution_phase(self):
        # Sort the turn queue based on action type and creature speed
        self.turn_queue.sort(key=lambda x: ("swap" in x, -x[1].active_creature.speed, random.random()))
        
        for action in self.turn_queue:
            if action[0] == "swap":
                player, new_creature = action[1], action[2]
                player.active_creature = new_creature
                self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")
            elif action[0] == "attack":
                attacker, skill = action[1], action[2]
                defender = self.player if attacker == self.opponent else self.opponent
                damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
                defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
                self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage to {defender.display_name}'s {defender.active_creature.display_name}!")
                if defender.active_creature.hp == 0:
                    self._handle_knockout(defender)
        self.turn_queue.clear()

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        type_effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def _get_type_effectiveness(self, skill_type: str, defender_type: str) -> float:
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def _handle_knockout(self, player: Player):
        self._show_text(self.player, f"{player.display_name}'s {player.active_creature.display_name} was knocked out!")
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if available_creatures:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            creature_choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = creature_choice.thing
            self._show_text(self.player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        else:
            self._show_text(self.player, f"{player.display_name} has no more creatures left!")

    def _check_battle_end(self) -> bool:
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def _end_battle(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
        self._transition_to_scene("MainMenuScene")
