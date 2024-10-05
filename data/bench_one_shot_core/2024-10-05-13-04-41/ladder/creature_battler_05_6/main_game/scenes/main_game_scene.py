from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.foe.active_creature = self.foe.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
{self.foe.display_name}: {self.foe.active_creature.display_name} (HP: {self.foe.active_creature.hp}/{self.foe.active_creature.max_hp})

> Attack
> Swap
"""

    def run(self):
        while True:
            player_action = self.player_choice_phase(self.player)
            foe_action = self.player_choice_phase(self.foe)
            if self.resolution_phase(player_action, foe_action):
                break
            if self.check_battle_end():
                break
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self, current_player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choices = [attack_button, swap_button]
        choice = self._wait_for_choice(current_player, choices)

        if choice == attack_button:
            return self.choose_attack(current_player)
        elif choice == swap_button:
            return self.choose_swap(current_player)

    def choose_attack(self, current_player):
        skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
        back_button = Button("Back")
        choices = skill_choices + [back_button]
        choice = self._wait_for_choice(current_player, choices)

        if choice == back_button:
            return self.player_choice_phase(current_player)
        return ("attack", choice.thing)

    def choose_swap(self, current_player):
        available_creatures = [creature for creature in current_player.creatures if creature.hp > 0 and creature != current_player.active_creature]
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        choices = creature_choices + [back_button]
        choice = self._wait_for_choice(current_player, choices)

        if choice == back_button:
            return self.player_choice_phase(current_player)
        return ("swap", choice.thing)

    def resolution_phase(self, player_action, foe_action):
        actions = [
            (self.player, player_action),
            (self.foe, foe_action)
        ]
        
        # Sort actions based on type (swap first) and creature speed (with randomness for equal speeds)
        actions.sort(key=lambda x: self.action_priority(x[0], x[1]), reverse=True)

        for actor, action in actions:
            if action[0] == "swap":
                self.perform_swap(actor, action[1])
            elif action[0] == "attack":
                defender = self.foe if actor == self.player else self.player
                if self.perform_attack(actor, defender, action[1]):
                    return True  # Battle ended due to knockout

        return False  # Battle continues

    def action_priority(self, player, action):
        if action[0] == "swap":
            return (float('inf'), 0)  # Swaps always go first
        else:  # attack
            return (player.active_creature.speed, random.random())

    def perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(player, f"{player.display_name} swapped to {new_creature.display_name}!")

    def perform_attack(self, attacker, defender, skill):
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(defender, f"{defender.active_creature.display_name} was knocked out!")
            if not self.force_swap(defender):
                self._show_text(defender, f"{defender.display_name} has no more creatures left!")
                return True  # Battle ended
        return False  # Battle continues

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
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
        return False

    def force_swap(self, player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if not available_creatures:
            return False
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        self._show_text(player, f"{player.display_name} swapped to {player.active_creature.display_name}!")
        return True

    def reset_creatures(self):
        for player in [self.player, self.foe]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
