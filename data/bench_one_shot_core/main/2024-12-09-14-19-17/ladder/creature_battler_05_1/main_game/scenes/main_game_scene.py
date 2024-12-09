from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, BotListener
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
        
        # Sort by speed for attack order, using random tiebreaker for equal speeds
        actions.sort(key=lambda x: (x[1].active_creature.speed, random.random()), reverse=True)
        
        for action, attacker, defender in actions:
            if not action or isinstance(action, Creature):
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
                
            self._show_text(player, f"{player.active_creature.display_name} fainted!")
            if isinstance(player._listener, BotListener):
                player.active_creature = random.choice(available)
            else:
                choices = [SelectThing(c) for c in available]
                player.active_creature = self._wait_for_choice(player, choices).thing
            self._show_text(player, f"Go, {player.active_creature.display_name}!")
        return True

    def get_player_action(self):
        while True:
            # Main choice menu
            choices = [Button("Attack")]
            if self.get_available_creatures(self.player):
                choices.append(Button("Swap"))
            
            main_choice = self._wait_for_choice(self.player, choices)

            if main_choice.display_name == "Attack":
                # Show skills with Back option
                choices = [SelectThing(s) for s in self.player.active_creature.skills]
                choices.append(Button("Back"))
                choice = self._wait_for_choice(self.player, choices)
                
                if isinstance(choice, Button):
                    continue
                return choice.thing

            elif main_choice.display_name == "Swap":
                # Show available creatures with Back option
                available = self.get_available_creatures(self.player)
                choices = [SelectThing(c) for c in available]
                choices.append(Button("Back"))
                choice = self._wait_for_choice(self.player, choices)
                
                if isinstance(choice, Button):
                    continue
                return choice.thing

    def run(self):
        while True:
            # Player turn with Back option support
            p1_action = self.get_player_action()

            # Bot turn
            if random.random() < 0.2 and self.get_available_creatures(self.bot):
                p2_action = random.choice(self.get_available_creatures(self.bot))
            else:
                p2_action = random.choice(self.bot.active_creature.skills)

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
