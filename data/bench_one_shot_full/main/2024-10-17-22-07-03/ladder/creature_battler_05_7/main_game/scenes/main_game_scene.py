from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")

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
        self.setup_battle()
        self.battle_loop()
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def setup_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def battle_loop(self):
        while True:
            player_action = self.player_choice_phase()
            opponent_action = self.foe_choice_phase()
            self.resolution_phase(player_action, opponent_action)
            if self.check_battle_end():
                break

    def player_choice_phase(self):
        return self.get_player_action(self.player)

    def foe_choice_phase(self):
        return self.get_player_action(self.opponent)

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if attack_button == choice:
                skill = self.choose_skill(player)
                if skill:
                    return ("attack", skill)
            elif swap_button == choice:
                new_creature = self.choose_swap_creature(player)
                if new_creature:
                    return ("swap", new_creature)

    def choose_skill(self, player):
        skills = player.active_creature.skills
        choices = [SelectThing(skill, label=skill.display_name) for skill in skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def choose_swap_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature, label=creature.display_name) for creature in available_creatures]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def resolution_phase(self, player_action, opponent_action):
        turn_queue = [
            (self.player, *player_action),
            (self.opponent, *opponent_action)
        ]
        turn_queue.sort(key=lambda x: (x[1] != "swap", -x[0].active_creature.speed, random.random()))
        for player, action_type, action in turn_queue:
            if action_type == "swap":
                self.perform_swap(player, action)
            elif action_type == "attack":
                self.perform_attack(player, action)

    def perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def perform_attack(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        return int(raw_damage * type_factor)

    def get_type_factor(self, skill_type, creature_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)

    def check_battle_end(self):
        for player in [self.player, self.opponent]:
            if all(creature.hp == 0 for creature in player.creatures):
                winner = self.opponent if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins the battle!")
                return True
            if player.active_creature.hp == 0:
                self.force_swap(player)
        return False

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            choices = [SelectThing(creature, label=creature.display_name) for creature in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
