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
> Swap"""

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
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            
            self._show_text(attacker, f"{attacker.active_creature.display_name} used {action.display_name}!")
            self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")

    def get_available_creatures(self, player: Player) -> list[Creature]:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_player_turn(self, player: Player) -> tuple[any, bool]:
        while True:
            choice = self._wait_for_choice(player, [
                Button("Attack"),
                Button("Swap")
            ])

            if isinstance(choice, Button) and choice.display_name == "Attack":
                skills = [SelectThing(s) for s in player.active_creature.skills]
                skills.append(Button("Back"))
                
                skill_choice = self._wait_for_choice(player, skills)
                if isinstance(skill_choice, Button) and skill_choice.display_name == "Back":
                    continue
                    
                if isinstance(skill_choice, SelectThing):
                    return skill_choice.thing, False

            else:  # Swap
                available = [SelectThing(c) for c in self.get_available_creatures(player)]
                if not available:
                    self._show_text(player, "No creatures available to swap to!")
                    continue
                    
                available.append(Button("Back"))
                swap_choice = self._wait_for_choice(player, available)
                
                if isinstance(swap_choice, Button) and swap_choice.display_name == "Back":
                    continue
                    
                if isinstance(swap_choice, SelectThing):
                    return swap_choice.thing, False

    def force_swap(self, player: Player) -> bool:
        available = self.get_available_creatures(player)
        if not available:
            return True
            
        choice = self._wait_for_choice(player, [SelectThing(c) for c in available])
        if isinstance(choice, SelectThing):
            player.active_creature = choice.thing
        return False

    def run(self):
        while True:
            # Player turn
            p1_action, p1_done = self.handle_player_turn(self.player)
            if p1_done:
                self._show_text(self.player, "You lost!")
                break

            # Bot turn  
            p2_action, p2_done = self.handle_player_turn(self.bot)
            if p2_done:
                self._show_text(self.player, "You won!")
                break

            # Execute turn
            self.execute_turn(p1_action, p2_action)

            # Check for knockouts
            for player in [self.player, self.bot]:
                if player.active_creature.hp <= 0:
                    self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
                    if self.force_swap(player):
                        self._show_text(self.player, "Game Over!")
                        self.reset_creatures()
                        self._transition_to_scene("MainMenuScene")
                        return
