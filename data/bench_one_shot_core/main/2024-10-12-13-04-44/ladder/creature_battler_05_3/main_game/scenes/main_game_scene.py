from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
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
            self.player_turn()
            self.opponent_turn()
            self.resolve_turn()
            
            if self.check_battle_end():
                break

        self.reset_creatures_hp()
        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(self.player, choices)

            if choice == attack_button:
                skill = self.choose_skill(self.player)
                if skill:
                    self.turn_queue.append(("attack", self.player, skill))
                    break
            elif choice == swap_button:
                new_creature = self.choose_creature(self.player)
                if new_creature:
                    self.turn_queue.append(("swap", self.player, new_creature))
                    break

    def opponent_turn(self):
        choices = [Button("Attack"), Button("Swap")]
        choice = self._wait_for_choice(self.opponent, choices)

        if choice.display_name == "Attack":
            skills = self.opponent.active_creature.skills
            skill = self._wait_for_choice(self.opponent, [SelectThing(s) for s in skills])
            self.turn_queue.append(("attack", self.opponent, skill.thing))
        else:
            available_creatures = [c for c in self.opponent.creatures if c.hp > 0 and c != self.opponent.active_creature]
            if available_creatures:
                new_creature = self._wait_for_choice(self.opponent, [SelectThing(c) for c in available_creatures])
                self.turn_queue.append(("swap", self.opponent, new_creature.thing))

    def resolve_turn(self):
        def sort_key(action):
            action_type, player, thing = action
            priority = -1 if action_type == "swap" else 0
            speed = player.active_creature.speed if action_type == "attack" else 0
            return (priority, speed, random.random())

        self.turn_queue.sort(key=sort_key, reverse=True)

        for action in self.turn_queue:
            action_type, player, thing = action
            if action_type == "swap":
                player.active_creature = thing
                self._show_text(self.player, f"{player.display_name} swapped to {thing.display_name}!")
                self._show_text(self.opponent, f"{player.display_name} swapped to {thing.display_name}!")
            elif action_type == "attack":
                attacker = player
                defender = self.player if attacker == self.opponent else self.opponent
                skill = thing
                damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
                defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
                self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
                self._show_text(self.opponent, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
                self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} took {damage} damage!")
                self._show_text(self.opponent, f"{defender.display_name}'s {defender.active_creature.display_name} took {damage} damage!")

                if defender.active_creature.hp == 0:
                    self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
                    self._show_text(self.opponent, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
                    if not self.force_swap(defender):
                        return

        self.turn_queue.clear()

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_effectiveness(self, skill_type: str, defender_type: str) -> float:
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def force_swap(self, player: Player) -> bool:
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not available_creatures:
            return False

        self._show_text(self.player, f"{player.display_name} must choose a new creature!")
        self._show_text(self.opponent, f"{player.display_name} must choose a new creature!")
        new_creature = self._wait_for_choice(player, [SelectThing(c) for c in available_creatures])
        player.active_creature = new_creature.thing
        self._show_text(self.player, f"{player.display_name} sent out {new_creature.thing.display_name}!")
        self._show_text(self.opponent, f"{player.display_name} sent out {new_creature.thing.display_name}!")
        return True

    def check_battle_end(self) -> bool:
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            return True
        elif all(c.hp == 0 for c in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            return True
        return False

    def choose_skill(self, player: Player) -> Skill | None:
        skills = player.active_creature.skills
        skill_choices = [SelectThing(s) for s in skills]
        skill_choices.append(Button("Back"))
        choice = self._wait_for_choice(player, skill_choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def choose_creature(self, player: Player) -> Creature | None:
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not available_creatures:
            self._show_text(player, "No other creatures available!")
            return None
        creature_choices = [SelectThing(c) for c in available_creatures]
        creature_choices.append(Button("Back"))
        choice = self._wait_for_choice(player, creature_choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def reset_creatures_hp(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
