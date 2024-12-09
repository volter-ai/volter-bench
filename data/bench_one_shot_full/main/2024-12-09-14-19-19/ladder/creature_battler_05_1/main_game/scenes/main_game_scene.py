from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
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
> Swap
"""

    def _get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        return int(raw_damage * multiplier)

    def _handle_attack(self, attacker: Player, defender: Player) -> tuple[Creature, int]:
        choices = [SelectThing(s) for s in attacker.active_creature.skills]
        choices.append(Button("Back"))
        
        choice = self._wait_for_choice(attacker, choices)
        if isinstance(choice, Button):
            return None, 0
            
        skill = choice.thing
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        return skill, damage

    def _handle_swap(self, player: Player) -> Creature:
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not available_creatures:
            return None
            
        choices = [SelectThing(c) for c in available_creatures]
        choices.append(Button("Back"))
        
        choice = self._wait_for_choice(player, choices)
        if isinstance(choice, Button):
            return None
            
        return choice.thing

    def _force_swap(self, player: Player) -> bool:
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return False
            
        choices = [SelectThing(c) for c in available_creatures]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return True

    def _execute_turn(self, first: Player, second: Player, first_action: tuple, second_action: tuple):
        # Handle swaps first
        if isinstance(first_action, Creature):
            first.active_creature = first_action
        if isinstance(second_action, Creature):
            second.active_creature = second_action

        # Then handle attacks
        if isinstance(first_action, tuple):
            skill, damage = first_action
            if skill is not None:  # Only show message if there was an actual attack
                second.active_creature.hp -= damage
                self._show_text(first, f"{first.active_creature.display_name} used {skill.display_name} for {damage} damage!")
            
        if isinstance(second_action, tuple) and second.active_creature.hp > 0:
            skill, damage = second_action
            if skill is not None:  # Only show message if there was an actual attack
                first.active_creature.hp -= damage
                self._show_text(second, f"{second.active_creature.display_name} used {skill.display_name} for {damage} damage!")

    def run(self):
        while True:
            # Player turn
            while True:  # Keep asking for action until valid one chosen
                attack_button = Button("Attack")
                swap_button = Button("Swap")
                player_choice = self._wait_for_choice(self.player, [attack_button, swap_button])
                
                player_action = None
                if player_choice == attack_button:
                    player_action = self._handle_attack(self.player, self.bot)
                else:
                    player_action = self._handle_swap(self.player)
                    
                if player_action is not None and (not isinstance(player_action, tuple) or player_action[0] is not None):
                    break

            # Bot turn
            if random.random() < 0.2 and len([c for c in self.bot.creatures if c.hp > 0]) > 1:
                bot_action = self._handle_swap(self.bot)
            else:
                bot_action = self._handle_attack(self.bot, self.player)

            # Determine turn order
            if (isinstance(player_action, Creature) or isinstance(bot_action, Creature) or 
                self.player.active_creature.speed == self.bot.active_creature.speed):
                first, second = self.player, self.bot
                first_action, second_action = player_action, bot_action
            elif self.player.active_creature.speed > self.bot.active_creature.speed:
                first, second = self.player, self.bot
                first_action, second_action = player_action, bot_action
            else:
                first, second = self.bot, self.player
                first_action, second_action = bot_action, player_action

            self._execute_turn(first, second, first_action, second_action)

            # Handle fainted creatures
            for p in [self.player, self.bot]:
                if p.active_creature.hp <= 0:
                    self._show_text(p, f"{p.active_creature.display_name} fainted!")
                    if not self._force_swap(p):
                        winner = self.bot if p == self.player else self.player
                        self._show_text(self.player, f"{winner.display_name} wins!")
                        self._transition_to_scene("MainMenuScene")
                        return
