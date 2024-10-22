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
        self.setup_battle()
        self.battle_loop()

    def setup_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.opponent.active_creature = self.opponent.creatures[0]

    def battle_loop(self):
        while True:
            self.player_turn()
            self.opponent_turn()
            self.resolve_turn()
            if self.check_battle_end():
                break
        self.end_battle()

    def player_turn(self):
        while True:
            action_choice = self._wait_for_choice(self.player, [Button("Attack"), Button("Swap")])
            if action_choice.display_name == "Attack":
                skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                skill_choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                if isinstance(skill_choice, SelectThing):
                    self.turn_queue.append((self.player, "attack", skill_choice.thing))
                    break
            elif action_choice.display_name == "Swap":
                creature_choices = [SelectThing(creature) for creature in self.player.creatures if creature != self.player.active_creature and creature.hp > 0]
                creature_choices.append(Button("Back"))
                creature_choice = self._wait_for_choice(self.player, creature_choices)
                if isinstance(creature_choice, SelectThing):
                    self.turn_queue.append((self.player, "swap", creature_choice.thing))
                    break

    def opponent_turn(self):
        action_choice = random.choice(["attack", "swap"])
        if action_choice == "attack":
            skill = random.choice(self.opponent.active_creature.skills)
            self.turn_queue.append((self.opponent, "attack", skill))
        else:
            available_creatures = [c for c in self.opponent.creatures if c != self.opponent.active_creature and c.hp > 0]
            if available_creatures:
                creature = random.choice(available_creatures)
                self.turn_queue.append((self.opponent, "swap", creature))
            else:
                skill = random.choice(self.opponent.active_creature.skills)
                self.turn_queue.append((self.opponent, "attack", skill))

    def resolve_turn(self):
        # Shuffle the turn queue to randomize order for equal speeds
        random.shuffle(self.turn_queue)
        
        # Sort the turn queue, considering both action type and speed
        # Use a random factor for tiebreaking when speeds are equal
        self.turn_queue.sort(key=lambda x: (
            x[1] != "swap",  # Swap actions go first
            -x[0].active_creature.speed,  # Higher speed goes first
            random.random()  # Random tiebreaker for equal speeds
        ))
        
        for turn in self.turn_queue:
            player, action, target = turn
            if action == "swap":
                self._show_text(player, f"{player.display_name} swapped to {target.display_name}!")
                player.active_creature = target
            elif action == "attack":
                self.execute_skill(player, target)
        self.turn_queue.clear()

    def execute_skill(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
        
        type_factor = self.get_type_factor(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * type_factor)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.display_name}'s {defender.active_creature.display_name} took {final_damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(defender, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
            self.force_swap(defender)

    def get_type_factor(self, skill_type, creature_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1)

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        else:
            self._show_text(player, f"{player.display_name} has no more creatures able to battle!")

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def end_battle(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
        self._transition_to_scene("MainMenuScene")
