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
        self._show_text(self.player, "Battle start!")
        self._show_text(self.opponent, "Battle start!")
        
        while True:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()
            
            if self.check_battle_end():
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        self.get_player_action(self.player)

    def foe_choice_phase(self):
        self.get_player_action(self.opponent)

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if attack_button == choice:
                skill = self.choose_skill(player)
                if skill:
                    self.turn_queue.append((player, "attack", skill))
                    break
            elif swap_button == choice:
                new_creature = self.choose_swap_creature(player)
                if new_creature:
                    self.turn_queue.append((player, "swap", new_creature))
                    break

    def choose_skill(self, player):
        skills = player.active_creature.skills
        choices = [SelectThing(skill, label=skill.display_name) for skill in skills]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        
        if isinstance(choice, SelectThing):
            return choice.thing
        return None

    def choose_swap_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature, label=creature.display_name) for creature in available_creatures]
        choices.append(Button("Back"))
        choice = self._wait_for_choice(player, choices)
        
        if isinstance(choice, SelectThing):
            return choice.thing
        return None

    def resolution_phase(self):
        def speed_key(action):
            player, action_type, _ = action
            if action_type == "swap":
                return (0, 0)  # Swaps always go first
            return (1, -player.active_creature.speed, random.random())  # Random tiebreaker

        self.turn_queue.sort(key=speed_key)
        
        for player, action_type, action in self.turn_queue:
            if action_type == "swap":
                self.perform_swap(player, action)
            elif action_type == "attack":
                self.perform_attack(player, action)

        self.turn_queue.clear()

    def perform_swap(self, player, new_creature):
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped to {new_creature.display_name}!")
        self._show_text(self.opponent, f"{player.display_name} swapped to {new_creature.display_name}!")

    def perform_attack(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        
        self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.opponent, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} took {damage} damage!")
        self._show_text(self.opponent, f"{defender.display_name}'s {defender.active_creature.display_name} took {damage} damage!")

        if defender.active_creature.hp == 0:
            self.handle_knockout(defender)

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = float(attacker.attack) + float(skill.base_damage) - float(defender.defense)
        else:
            raw_damage = (float(attacker.sp_attack) / float(defender.sp_defense)) * float(skill.base_damage)

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(float(type_factor) * raw_damage)
        return max(1, final_damage)

    def get_type_factor(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, player):
        self._show_text(self.player, f"{player.display_name}'s {player.active_creature.display_name} was knocked out!")
        self._show_text(self.opponent, f"{player.display_name}'s {player.active_creature.display_name} was knocked out!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            choices = [SelectThing(creature, label=creature.display_name) for creature in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(self.player, f"{player.display_name} sent out {player.active_creature.display_name}!")
            self._show_text(self.opponent, f"{player.display_name} sent out {player.active_creature.display_name}!")

    def check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            return True
        return False

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
            player.active_creature = player.creatures[0]
