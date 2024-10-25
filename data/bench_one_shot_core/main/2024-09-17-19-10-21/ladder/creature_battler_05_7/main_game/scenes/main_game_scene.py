from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.foe.active_creature = self.foe.creatures[0]
        self.turn_actions = []

    def __str__(self):
        player_creature = self.player.active_creature
        foe_creature = self.foe.active_creature
        return f"""===Battle===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {foe_creature.display_name}: HP {foe_creature.hp}/{foe_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._show_text(self.player, f"A wild {self.foe.display_name} appeared!")
        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()
            
            if self.check_battle_end():
                break
        self._quit_whole_game()

    def player_choice_phase(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if attack_button == choice:
                skill = self.choose_skill(self.player)
                if skill:
                    self.turn_actions.append(("attack", self.player, skill))
                    break
            elif swap_button == choice:
                new_creature = self.choose_creature(self.player)
                if new_creature:
                    self.turn_actions.append(("swap", self.player, new_creature))
                    break

    def foe_choice_phase(self):
        choices = ["attack", "swap"]
        choice = random.choice(choices)
        
        if choice == "attack":
            skill = random.choice(self.foe.active_creature.skills)
            self.turn_actions.append(("attack", self.foe, skill))
        else:
            available_creatures = [c for c in self.foe.creatures if c != self.foe.active_creature and c.hp > 0]
            if available_creatures:
                new_creature = random.choice(available_creatures)
                self.turn_actions.append(("swap", self.foe, new_creature))
            else:
                skill = random.choice(self.foe.active_creature.skills)
                self.turn_actions.append(("attack", self.foe, skill))

    def resolution_phase(self):
        # Sort actions: swaps first, then by speed
        self.turn_actions.sort(key=lambda x: (
            0 if x[0] == "swap" else 1,
            -x[2].speed if x[0] == "swap" else -x[1].active_creature.speed
        ))
        
        for action, player, target in self.turn_actions:
            if action == "swap":
                self.swap_creature(player, target)
            else:
                self.execute_skill(player, target)
        
        self.turn_actions.clear()

    def choose_skill(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        
        if isinstance(choice, SelectThing):
            return choice.thing
        return None

    def choose_creature(self, player):
        choices = [SelectThing(creature) for creature in player.creatures if creature != player.active_creature and creature.hp > 0]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        
        if isinstance(choice, SelectThing):
            return choice.thing
        return None

    def swap_creature(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def execute_skill(self, attacker, skill):
        defender = self.foe if attacker == self.player else self.player
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.active_creature.display_name} took {damage} damage!")

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
        
        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_factor)
        return max(1, final_damage)

    def get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.foe.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        
        if self.player.active_creature.hp == 0:
            self.force_swap(self.player)
        if self.foe.active_creature.hp == 0:
            self.force_swap(self.foe)
        
        return False

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            if player == self.player:
                new_creature = self.choose_creature(player)
                if new_creature:
                    self.swap_creature(player, new_creature)
            else:
                new_creature = random.choice(available_creatures)
                self.swap_creature(player, new_creature)
