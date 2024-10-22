import random

from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.turn_queue = []

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        return f"""===Main Game===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.bot.display_name}'s {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self.setup_battle()
        self.game_loop()
        self.reset_creatures()

    def setup_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def game_loop(self):
        while True:
            self.player_choice_phase(self.player)
            self.player_choice_phase(self.bot)
            self.resolution_phase()

            if self.check_battle_end():
                break

        # Transition back to MainMenuScene when the battle ends
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if attack_button == choice:
                skill = self.choose_skill(current_player)
                if skill:
                    self.turn_queue.append((current_player.uid, "attack", skill.prototype_id))
                    break
            elif swap_button == choice:
                new_creature = self.choose_creature(current_player)
                if new_creature:
                    self.turn_queue.append((current_player.uid, "swap", new_creature.prototype_id))
                    break

    def choose_skill(self, player):
        skills = player.active_creature.skills
        choices = [SelectThing(skill) for skill in skills] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def choose_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def resolution_phase(self):
        self.turn_queue.sort(key=lambda x: (x[1] != "swap", -self.get_player(x[0]).active_creature.speed, random.random()))
        
        for player_uid, action, target_id in self.turn_queue:
            player = self.get_player(player_uid)
            if action == "swap":
                new_creature = next(c for c in player.creatures if c.prototype_id == target_id)
                player.active_creature = new_creature
                self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")
            elif action == "attack":
                skill = next(s for s in player.active_creature.skills if s.prototype_id == target_id)
                self.execute_attack(player, skill)

        self.turn_queue.clear()

    def get_player(self, player_uid):
        return self.player if player_uid == self.player.uid else self.bot

    def execute_attack(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        defender_creature = defender.active_creature

        if skill.is_physical:
            raw_damage = float(attacker.active_creature.attack + skill.base_damage - defender_creature.defense)
        else:
            raw_damage = float(attacker.active_creature.sp_attack) / float(defender_creature.sp_defense) * float(skill.base_damage)

        weakness_factor = self.calculate_weakness(skill.skill_type, defender_creature.creature_type)
        final_damage = int(float(weakness_factor) * raw_damage)

        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} took {final_damage} damage!")

        if defender_creature.hp == 0:
            self._show_text(defender, f"{defender.display_name}'s {defender_creature.display_name} fainted!")
            self.force_swap(defender)

    def calculate_weakness(self, skill_type, creature_type):
        weakness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return float(weakness_chart.get(skill_type, {}).get(creature_type, 1.0))

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return

        choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")

    def check_battle_end(self):
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
