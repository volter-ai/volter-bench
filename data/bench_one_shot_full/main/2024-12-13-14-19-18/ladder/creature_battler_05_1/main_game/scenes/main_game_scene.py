from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
from typing import List, Tuple
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self._reset_creatures()

    def _reset_creatures(self):
        # Reset all creatures to full HP
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

    def __str__(self):
        p1 = self.player
        p2 = self.bot
        return f"""=== Battle ===
{p1.display_name}'s {p1.active_creature.display_name}: {p1.active_creature.hp}/{p1.active_creature.max_hp} HP
{p2.display_name}'s {p2.active_creature.display_name}: {p2.active_creature.hp}/{p2.active_creature.max_hp} HP

> Attack
> Swap"""

    def _calculate_damage(self, skill: Skill, attacker: Creature, defender: Creature) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Calculate type multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": multiplier = 2.0
            elif defender.creature_type == "water": multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": multiplier = 2.0
            elif defender.creature_type == "leaf": multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": multiplier = 2.0
            elif defender.creature_type == "fire": multiplier = 0.5

        return int(raw_damage * multiplier)

    def _get_available_creatures(self, player: Player) -> List[Creature]:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def _handle_turn(self, player: Player) -> Tuple[str, Skill | Creature | None]:
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")

        while True:
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                skill_choices = [SelectThing(s) for s in player.active_creature.skills]
                skill_choices.append(back_button)
                choice = self._wait_for_choice(player, skill_choices)
                if choice == back_button:
                    continue
                return "attack", choice.thing

            elif choice == swap_button:
                creature_choices = [SelectThing(c) for c in self._get_available_creatures(player)]
                creature_choices.append(back_button)
                if not creature_choices:
                    self._show_text(player, "No creatures available to swap!")
                    continue
                choice = self._wait_for_choice(player, creature_choices)
                if choice == back_button:
                    continue
                return "swap", choice.thing

    def _check_game_over(self) -> bool:
        for p in [self.player, self.bot]:
            if all(c.hp <= 0 for c in p.creatures):
                winner = self.bot if p == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                return True
        return False

    def run(self):
        while True:
            # Get actions from both players
            p1_action, p1_target = self._handle_turn(self.player)
            p2_action, p2_target = self._handle_turn(self.bot)

            # Handle swaps first
            for p, action, target in [(self.player, p1_action, p1_target), (self.bot, p2_action, p2_target)]:
                if action == "swap":
                    p.active_creature = target
                    self._show_text(self.player, f"{p.display_name} swapped to {target.display_name}!")

            # Handle attacks in speed order
            actions = [(self.player, p1_action, p1_target), (self.bot, p2_action, p2_target)]
            actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
            
            for attacker, action, skill in actions:
                if action == "attack":
                    defender = self.bot if attacker == self.player else self.player
                    damage = self._calculate_damage(skill, attacker.active_creature, defender.active_creature)
                    defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
                    self._show_text(self.player, 
                        f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}! "
                        f"Dealt {damage} damage to {defender.display_name}'s {defender.active_creature.display_name}!")

                    if defender.active_creature.hp <= 0:
                        self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
                        available = self._get_available_creatures(defender)
                        if available:
                            swap_choices = [SelectThing(c) for c in available]
                            choice = self._wait_for_choice(defender, swap_choices)
                            defender.active_creature = choice.thing
                            self._show_text(self.player, f"{defender.display_name} sent out {choice.thing.display_name}!")

            if self._check_game_over():
                self._reset_creatures()
                self._transition_to_scene("MainMenuScene")
                return
