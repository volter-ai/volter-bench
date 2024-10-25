from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]
        self.player_action = None
        self.opponent_action = None

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
{self.opponent.display_name}: {self.opponent.active_creature.display_name} (HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp})

> Attack
> Swap
"""

    def run(self):
        while True:
            self.check_and_force_swap(self.player)
            self.check_and_force_swap(self.opponent)
            if self.check_battle_end():
                break
            self.player_turn()
            self.opponent_turn()
            self.resolution_phase()
            if self.check_battle_end():
                break

    def player_turn(self):
        self.player_action = self.get_player_action(self.player)

    def opponent_turn(self):
        self.opponent_action = self.get_player_action(self.opponent)

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if attack_button == choice:
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choice = self._wait_for_choice(player, skill_choices + [Button("Back")])
                if isinstance(skill_choice, SelectThing):
                    return ("attack", skill_choice.thing)
            elif swap_button == choice:
                creature_choices = [SelectThing(creature) for creature in player.creatures if creature != player.active_creature and creature.hp > 0]
                creature_choice = self._wait_for_choice(player, creature_choices + [Button("Back")])
                if isinstance(creature_choice, SelectThing):
                    return ("swap", creature_choice.thing)

    def resolution_phase(self):
        actions = [
            (self.player, self.player_action),
            (self.opponent, self.opponent_action)
        ]
        
        actions.sort(key=lambda x: (x[0].active_creature.speed, random.random()), reverse=True)

        for player, action in actions:
            if action[0] == "swap":
                player.active_creature = action[1]
                self._show_text(player, f"{player.display_name} swapped to {action[1].display_name}!")
            elif action[0] == "attack":
                self.execute_skill(player, action[1])
                self.check_and_force_swap(self.player)
                self.check_and_force_swap(self.opponent)

        self.player_action = None
        self.opponent_action = None

    def execute_skill(self, attacker, skill):
        defender = self.opponent if attacker == self.player else self.player
        
        if skill.is_physical:
            raw_damage = float(attacker.active_creature.attack) + float(skill.base_damage) - float(defender.active_creature.defense)
        else:
            raw_damage = (float(attacker.active_creature.sp_attack) / float(defender.active_creature.sp_defense)) * float(skill.base_damage)

        weakness_factor = self.get_weakness_factor(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {final_damage} damage!")

    def get_weakness_factor(self, skill_type, creature_type):
        weakness_chart = {
            "normal": {"normal": 1, "fire": 1, "water": 1, "leaf": 1},
            "fire": {"normal": 1, "fire": 1, "water": 0.5, "leaf": 2},
            "water": {"normal": 1, "fire": 2, "water": 1, "leaf": 0.5},
            "leaf": {"normal": 1, "fire": 0.5, "water": 2, "leaf": 1}
        }
        return weakness_chart.get(skill_type, {}).get(creature_type, 1)

    def check_and_force_swap(self, player):
        if player.active_creature.hp == 0:
            available_creatures = [c for c in player.creatures if c.hp > 0]
            if available_creatures:
                swap_choices = [SelectThing(creature) for creature in available_creatures]
                swap_choice = self._wait_for_choice(player, swap_choices)
                player.active_creature = swap_choice.thing
                self._show_text(player, f"{player.display_name} was forced to swap to {player.active_creature.display_name}!")

    def check_battle_end(self):
        for player in [self.player, self.opponent]:
            if all(creature.hp == 0 for creature in player.creatures):
                winner = self.opponent if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins the battle!")
                self.reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return True
        return False

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp

    def _transition_to_scene(self, scene_name: str):
        self.reset_creatures()
        super()._transition_to_scene(scene_name)
