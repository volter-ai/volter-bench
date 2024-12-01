from typing import List, Optional
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        # Initialize creatures for both players
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle Scene ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        while True:
            # Check for battle end
            if self._check_battle_end():
                return
                
            # Player turn
            player_action = self._handle_turn_choices(self.player)
            # Bot turn 
            bot_action = self._handle_turn_choices(self.bot)
            
            # Resolve actions
            self._resolve_actions(player_action, bot_action)

    def _handle_turn_choices(self, current_player: Player) -> DictionaryChoice:
        while True:
            # Main choice between Attack and Swap
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(current_player, [attack_button, swap_button])

            if choice == attack_button:
                # Show skills as choices
                skill_choices = [
                    SelectThing(skill) 
                    for skill in current_player.active_creature.skills
                ]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(current_player, [*skill_choices, back_button])
                
                if skill_choice == back_button:
                    continue
                    
                action = DictionaryChoice("Attack")
                action.value = {
                    "type": "attack",
                    "skill": skill_choice.thing
                }
                return action

            elif choice == swap_button:
                # Show available creatures as choices
                creature_choices = [
                    SelectThing(creature)
                    for creature in current_player.creatures
                    if creature != current_player.active_creature and creature.hp > 0
                ]
                
                if not creature_choices:
                    self._show_text(current_player, "No other creatures available!")
                    continue
                    
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(current_player, [*creature_choices, back_button])
                
                if creature_choice == back_button:
                    continue
                    
                action = DictionaryChoice("Swap")
                action.value = {
                    "type": "swap",
                    "creature": creature_choice.thing
                }
                return action

    def _resolve_actions(self, player_action: DictionaryChoice, bot_action: DictionaryChoice):
        actions = [player_action, bot_action]
        actors = [self.player, self.bot]
        
        # Handle swaps first
        for i, action in enumerate(actions):
            if action.value["type"] == "swap":
                actor = actors[i]
                new_creature = action.value["creature"]
                actor.active_creature = new_creature
                self._show_text(actor, f"Swapped to {new_creature.display_name}!")

        # Then handle attacks in speed order
        attack_actions = [(i, action) for i, action in enumerate(actions) if action.value["type"] == "attack"]
        if len(attack_actions) == 2:
            # Sort by speed
            attack_actions.sort(key=lambda x: actors[x[0]].active_creature.speed, reverse=True)
            
        for i, action in attack_actions:
            attacker = actors[i]
            defender = actors[1-i]
            skill = action.value["skill"]
            
            damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            
            self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
            self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")
            
            if defender.active_creature.hp == 0:
                self._handle_knockout(defender)

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def _get_type_multiplier(self, attack_type: str, defender_type: str) -> float:
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defender_type, 1.0)

    def _handle_knockout(self, player: Player):
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        
        # Find available creatures
        available_creatures = [
            creature for creature in player.creatures
            if creature.hp > 0 and creature != player.active_creature
        ]
        
        if not available_creatures:
            return
            
        # Force swap
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        self._show_text(player, f"Go, {player.active_creature.display_name}!")

    def _check_battle_end(self) -> bool:
        # Check if either player has all creatures knocked out
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
