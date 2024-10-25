from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
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
        self._show_text(self.player, "Battle Start!")
        while True:
            self.player_turn()
            if self.check_battle_end():
                break
            self.opponent_turn()
            if self.check_battle_end():
                break
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
                    self.turn_queue.append(("skill", self.player, skill))
                    break
            elif swap_button == choice:
                new_creature = self.choose_creature(self.player)
                if new_creature:
                    self.turn_queue.append(("swap", self.player, new_creature))
                    break

    def opponent_turn(self):
        choices = ["Attack", "Swap"]
        choice = random.choice(choices)
        if choice == "Attack":
            skill = random.choice(self.opponent.active_creature.skills)
            self.turn_queue.append(("skill", self.opponent, skill))
        else:
            available_creatures = [c for c in self.opponent.creatures if c.hp > 0 and c != self.opponent.active_creature]
            if available_creatures:
                new_creature = random.choice(available_creatures)
                self.turn_queue.append(("swap", self.opponent, new_creature))

    def resolve_turn(self):
        self.turn_queue.sort(key=lambda x: (-1 if x[0] == "swap" else x[1].active_creature.speed), reverse=True)
        for action in self.turn_queue:
            if action[0] == "swap":
                player, new_creature = action[1], action[2]
                player.active_creature = new_creature
                self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")
            elif action[0] == "skill":
                attacker, skill = action[1], action[2]
                defender = self.player if attacker == self.opponent else self.opponent
                damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
                defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
                self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
                self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} took {damage} damage!")
                if defender.active_creature.hp == 0:
                    self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
                    if not self.check_battle_end():
                        self.force_swap(defender)
        self.turn_queue.clear()

    def choose_skill(self, player):
        choices = [SelectThing(skill, label=skill.display_name) for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, SelectThing):
            return choice.thing
        return None

    def choose_creature(self, player):
        choices = [SelectThing(creature, label=creature.display_name) for creature in player.creatures if creature.hp > 0 and creature != player.active_creature]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, SelectThing):
            return choice.thing
        return None

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            if player == self.player:
                new_creature = self.choose_creature(player)
                while not new_creature:
                    self._show_text(player, "You must choose a new creature!")
                    new_creature = self.choose_creature(player)
            else:
                new_creature = random.choice(available_creatures)
            player.active_creature = new_creature
            self._show_text(self.player, f"{player.display_name} sent out {new_creature.display_name}!")

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

    def reset_creatures_state(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self.reset_creatures_state()
            self._transition_to_scene("MainMenuScene")
            return True
        elif all(creature.hp == 0 for creature in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            self.reset_creatures_state()
            self._transition_to_scene("MainMenuScene")
            return True
        return False
