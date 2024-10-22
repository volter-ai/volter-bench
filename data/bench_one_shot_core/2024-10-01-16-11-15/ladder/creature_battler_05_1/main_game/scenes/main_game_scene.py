import random

from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Main Game===
{self.player.display_name}: {self.player.active_creature.display_name} (HP: {self.player.active_creature.hp}/{self.player.active_creature.max_hp})
{self.opponent.display_name}: {self.opponent.active_creature.display_name} (HP: {self.opponent.active_creature.hp}/{self.opponent.active_creature.max_hp})

> Attack
> Swap
"""

    def run(self):
        self.game_loop()
        self.reset_creatures_state()
        self._transition_to_scene("MainMenuScene")

    def game_loop(self):
        while True:
            turn_actions = []
            self.player_choice_phase(self.player, turn_actions)
            self.player_choice_phase(self.opponent, turn_actions)
            self.resolution_phase(turn_actions)
            
            if self.check_battle_end():
                break

    def player_choice_phase(self, current_player, turn_actions):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(current_player, choices)

            if attack_button == choice:
                skill = self.choose_skill(current_player)
                if skill:
                    turn_actions.append((current_player, "attack", skill))
                    break
            elif swap_button == choice:
                new_creature = self.choose_creature(current_player)
                if new_creature:
                    turn_actions.append((current_player, "swap", new_creature))
                    break

    def choose_skill(self, player):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def choose_creature(self, player):
        choices = [SelectThing(creature) for creature in player.creatures if creature != player.active_creature and creature.hp > 0]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def resolution_phase(self, turn_actions):
        speed_groups = {}
        for action in turn_actions:
            speed = action[0].active_creature.speed
            if speed not in speed_groups:
                speed_groups[speed] = []
            speed_groups[speed].append(action)
        
        for speed in speed_groups:
            random.shuffle(speed_groups[speed])
        
        sorted_actions = []
        for speed in sorted(speed_groups.keys(), reverse=True):
            sorted_actions.extend(speed_groups[speed])
        
        swap_actions = [action for action in sorted_actions if action[1] == "swap"]
        attack_actions = [action for action in sorted_actions if action[1] == "attack"]
        
        for action in swap_actions + attack_actions:
            player, action_type, action_data = action
            if action_type == "swap":
                player.active_creature = action_data
                self._show_text(player, f"{player.display_name} swapped to {action_data.display_name}!")
            elif action_type == "attack":
                self.execute_skill(player, action_data)

    def execute_skill(self, attacker, skill):
        defender = self.opponent if attacker == self.player else self.player
        
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        weakness_factor = self.get_weakness_factor(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {final_damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(defender, f"{defender.active_creature.display_name} was knocked out!")
            self.force_swap(defender)

    def get_weakness_factor(self, skill_type, creature_type):
        weakness_chart = {
            ("fire", "leaf"): 2,
            ("water", "fire"): 2,
            ("leaf", "water"): 2,
            ("fire", "water"): 0.5,
            ("water", "leaf"): 0.5,
            ("leaf", "fire"): 0.5
        }
        return weakness_chart.get((skill_type, creature_type), 1)

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            choices = [SelectThing(creature) for creature in available_creatures]
            self._show_text(player, f"Choose a creature to swap in:")
            choice = self._wait_for_choice(player, choices)
            new_creature = choice.thing
            player.active_creature = new_creature
            self._show_text(player, f"{player.display_name} sent out {new_creature.display_name}!")
        else:
            self._show_text(player, f"{player.display_name} has no more creatures able to fight!")

    def check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "All your creatures have been defeated. You lost the battle!")
            self._wait_for_choice(self.player, [Button("OK")])
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, "You have defeated all of your opponent's creatures. You won the battle!")
            self._wait_for_choice(self.player, [Button("OK")])
            return True
        return False

    def reset_creatures_state(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
