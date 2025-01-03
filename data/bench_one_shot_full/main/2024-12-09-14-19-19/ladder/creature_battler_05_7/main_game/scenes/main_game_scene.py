from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.reset_creatures()

    def reset_creatures(self):
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
{"> Swap" if self.get_available_creatures(p1) else ""}"""

    def get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def calculate_damage(self, attacker: Creature, defender: Creature, skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        return int(raw_damage * multiplier)

    def execute_turn(self, p1_action, p2_action):
        # Handle swaps first
        for action, player in [(p1_action, self.player), (p2_action, self.bot)]:
            if isinstance(action, Creature):
                player.active_creature = action
                self._show_text(player, f"{player.display_name} swapped to {action.display_name}!")

        # Then handle attacks
        actions = [(p1_action, self.player, self.bot), (p2_action, self.bot, self.player)]
        
        # Sort by speed for attack order
        actions.sort(key=lambda x: x[1].active_creature.speed, reverse=True)
        
        for action, attacker, defender in actions:
            if isinstance(action, Creature):
                continue
                
            damage = self.calculate_damage(attacker.active_creature, defender.active_creature, action)
            defender.active_creature.hp -= damage
            self._show_text(attacker, f"{attacker.active_creature.display_name} used {action.display_name}!")
            self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")

    def get_available_creatures(self, player: Player) -> list[Creature]:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_fainted(self, player: Player) -> bool:
        if player.active_creature.hp <= 0:
            available = self.get_available_creatures(player)
            if not available:
                return False
                
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        return True

    def run(self):
        while True:
            # Build available choices
            choices = [Button("Attack")]
            available_creatures = self.get_available_creatures(self.player)
            if available_creatures:
                choices.append(Button("Swap"))

            # Player turn
            choice = self._wait_for_choice(self.player, choices)

            p1_action = None
            if choice.display_name == "Attack":
                skills = [SelectThing(s) for s in self.player.active_creature.skills]
                p1_action = self._wait_for_choice(self.player, skills).thing
            else:  # Swap
                creatures = [SelectThing(c) for c in available_creatures]
                p1_action = self._wait_for_choice(self.player, creatures).thing

            # Bot turn
            if random.random() < 0.2 and self.get_available_creatures(self.bot):  # 20% chance to swap
                p2_action = random.choice(self.get_available_creatures(self.bot))
            else:
                p2_action = random.choice(self.bot.active_creature.skills)

            # Execute turn
            self.execute_turn(p1_action, p2_action)

            # Check for fainted creatures
            if not self.handle_fainted(self.player):
                self._show_text(self.player, "You lost!")
                break
            if not self.handle_fainted(self.bot):
                self._show_text(self.player, "You won!")
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")
