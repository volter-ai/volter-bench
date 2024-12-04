from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.type_effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5},
            "normal": {}
        }

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        # Initialize battle
        self._setup_battle()
        
        while True:
            # Get player and bot actions
            player_action = self._get_player_action(self.player)
            bot_action = self._get_player_action(self.bot)
            
            # Resolve actions
            self._resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                break

        # Reset creatures
        self._reset_creatures()

    def _setup_battle(self):
        for player in [self.player, self.bot]:
            player.active_creature = player.creatures[0]
            for creature in player.creatures:
                creature.hp = creature.max_hp

    def _get_player_action(self, player):
        while True:
            choice = self._wait_for_choice(player, [
                Button("Attack"),
                Button("Swap")
            ])

            if choice.display_name == "Attack":
                skills = [SelectThing(skill) for skill in player.active_creature.skills]
                skills.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skills)
                
                # Check if it's a Button (Back) or SelectThing
                if isinstance(skill_choice, Button):
                    if skill_choice.display_name == "Back":
                        continue
                else:
                    return ("attack", skill_choice.thing)
            else:
                available_creatures = [
                    SelectThing(c) for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                available_creatures.append(Button("Back"))
                swap_choice = self._wait_for_choice(player, available_creatures)
                
                # Check if it's a Button (Back) or SelectThing
                if isinstance(swap_choice, Button):
                    if swap_choice.display_name == "Back":
                        continue
                else:
                    return ("swap", swap_choice.thing)

    def _calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        effectiveness = self.type_effectiveness.get(skill.skill_type, {}).get(defender.creature_type, 1.0)
        
        return int(raw_damage * effectiveness)

    def _resolve_actions(self, player_action, bot_action):
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Handle swaps first
        for player, action in actions:
            if action[0] == "swap":
                player.active_creature = action[1]
                self._show_text(player, f"{player.display_name} swapped to {action[1].display_name}!")
        
        # Handle attacks based on speed
        attack_actions = [(p, a) for p, a in actions if a[0] == "attack"]
        if len(attack_actions) == 2:
            # Sort by speed
            attack_actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
            
        for attacker, action in attack_actions:
            if attacker == self.player:
                defender = self.bot
            else:
                defender = self.player
                
            damage = self._calculate_damage(attacker.active_creature, defender.active_creature, action[1])
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            
            self._show_text(attacker, f"{attacker.active_creature.display_name} used {action[1].display_name}!")
            self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")
            
            if defender.active_creature.hp == 0:
                self._handle_knockout(defender)

    def _handle_knockout(self, player):
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            swap_choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, swap_choices)
            player.active_creature = choice.thing
            self._show_text(player, f"Go, {player.active_creature.display_name}!")

    def _check_battle_end(self):
        for player in [self.player, self.bot]:
            if all(c.hp == 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                return True
        return False

    def _reset_creatures(self):
        for player in [self.player, self.bot]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
            player.active_creature = None
