from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Player
import random

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

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": effectiveness = 2.0
            elif defender.creature_type == "water": effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": effectiveness = 2.0
            elif defender.creature_type == "leaf": effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": effectiveness = 2.0
            elif defender.creature_type == "fire": effectiveness = 0.5

        return int(raw_damage * effectiveness)

    def _handle_turn(self, p1: Player, p2: Player):
        # Get actions
        p1_action = self._get_player_action(p1)
        p2_action = self._get_player_action(p2)

        # Handle swaps first
        if isinstance(p1_action, Creature):
            p1.active_creature = p1_action
        if isinstance(p2_action, Creature):
            p2.active_creature = p2_action

        # Handle attacks based on speed
        if not isinstance(p1_action, Creature) and not isinstance(p2_action, Creature):
            first = p1 if p1.active_creature.speed > p2.active_creature.speed or \
                        (p1.active_creature.speed == p2.active_creature.speed and random.random() < 0.5) else p2
            second = p2 if first == p1 else p1
            first_action = p1_action if first == p1 else p2_action
            second_action = p2_action if first == p1 else p1_action

            # Execute attacks
            damage = self._calculate_damage(first.active_creature, second.active_creature, first_action)
            second.active_creature.hp = max(0, second.active_creature.hp - damage)
            self._show_text(first, f"{first.active_creature.display_name} used {first_action.display_name}!")

            if second.active_creature.hp > 0:
                damage = self._calculate_damage(second.active_creature, first.active_creature, second_action)
                first.active_creature.hp = max(0, first.active_creature.hp - damage)
                self._show_text(second, f"{second.active_creature.display_name} used {second_action.display_name}!")

    def _get_player_action(self, player: Player):
        while True:
            choice = self._wait_for_choice(player, [
                Button("Attack"),
                Button("Swap"),
                Button("Back")
            ])

            if choice.display_name == "Attack":
                skills = [SelectThing(s) for s in player.active_creature.skills]
                skill_choice = self._wait_for_choice(player, skills + [Button("Back")])
                if isinstance(skill_choice, SelectThing):
                    return skill_choice.thing
            elif choice.display_name == "Swap":
                available = [SelectThing(c) for c in player.creatures 
                           if c.hp > 0 and c != player.active_creature]
                if available:
                    swap_choice = self._wait_for_choice(player, available + [Button("Back")])
                    if isinstance(swap_choice, SelectThing):
                        return swap_choice.thing

    def _handle_fainted(self, player: Player):
        if player.active_creature.hp <= 0:
            available = [c for c in player.creatures if c.hp > 0]
            if not available:
                return False
            self._show_text(player, f"{player.active_creature.display_name} fainted!")
            player.active_creature = self._wait_for_choice(
                player,
                [SelectThing(c) for c in available]
            ).thing
        return True

    def run(self):
        while True:
            self._handle_turn(self.player, self.bot)
            
            # Check for fainted creatures
            if not self._handle_fainted(self.player):
                self._show_text(self.player, "You lost!")
                break
            if not self._handle_fainted(self.bot):
                self._show_text(self.player, "You won!")
                break

        self._reset_creatures()
        self._transition_to_scene("MainMenuScene")
