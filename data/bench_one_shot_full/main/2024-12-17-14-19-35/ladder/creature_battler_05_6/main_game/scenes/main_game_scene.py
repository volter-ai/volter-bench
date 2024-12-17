from typing import List, Optional
from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        # Initialize active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        # Reset creature HPs
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creatures = [f"{c.display_name} (HP: {c.hp}/{c.max_hp})" for c in self.player.creatures]
        bot_creatures = [f"{c.display_name} (HP: {c.hp}/{c.max_hp})" for c in self.bot.creatures]
        
        return f"""=== Battle Scene ===
Your Team: {', '.join(player_creatures)}
Active: {self.player.active_creature.display_name if self.player.active_creature else 'None'}

Opponent's Team: {', '.join(bot_creatures)}
Active: {self.bot.active_creature.display_name if self.bot.active_creature else 'None'}
"""

    def run(self):
        while True:
            # Check for battle end
            if not self._has_available_creatures(self.player):
                self._show_text(self.player, "You lost the battle!")
                break
            if not self._has_available_creatures(self.bot):
                self._show_text(self.player, "You won the battle!")
                break

            # Player turn
            player_action = self._handle_turn_choice(self.player)
            if not player_action:
                break

            # Bot turn
            bot_action = self._handle_turn_choice(self.bot)
            if not bot_action:
                break

            # Resolution phase
            self._resolve_actions(player_action, bot_action)

        self._transition_to_scene("MainMenuScene")

    def _handle_turn_choice(self, current_player: Player) -> Optional[DictionaryChoice]:
        if current_player.active_creature.hp <= 0:
            available_creatures = [c for c in current_player.creatures if c.hp > 0]
            if not available_creatures:
                return None
            
            choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(current_player, choices)
            current_player.active_creature = choice.thing
            return DictionaryChoice("swap").value

        # Main choice
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choice = self._wait_for_choice(current_player, [attack_button, swap_button])

        if choice == attack_button:
            # Choose skill
            skill_choices = [SelectThing(s) for s in current_player.active_creature.skills]
            skill_choice = self._wait_for_choice(current_player, skill_choices)
            return DictionaryChoice("attack").value
        else:
            # Choose creature to swap to
            available_creatures = [c for c in current_player.creatures if c.hp > 0 and c != current_player.active_creature]
            if not available_creatures:
                return self._handle_turn_choice(current_player)
            
            creature_choices = [SelectThing(c) for c in available_creatures]
            creature_choice = self._wait_for_choice(current_player, creature_choices)
            current_player.active_creature = creature_choice.thing
            return DictionaryChoice("swap").value

    def _resolve_actions(self, player_action: dict, bot_action: dict):
        # Handle swaps first
        if player_action.get("swap"):
            self._show_text(self.player, f"You swapped to {self.player.active_creature.display_name}!")
        if bot_action.get("swap"):
            self._show_text(self.player, f"Opponent swapped to {self.bot.active_creature.display_name}!")

        # Then handle attacks based on speed
        if player_action.get("attack") and bot_action.get("attack"):
            if self.player.active_creature.speed >= self.bot.active_creature.speed:
                self._execute_attack(self.player, self.bot)
                if self.bot.active_creature.hp > 0:
                    self._execute_attack(self.bot, self.player)
            else:
                self._execute_attack(self.bot, self.player)
                if self.player.active_creature.hp > 0:
                    self._execute_attack(self.player, self.bot)

    def _execute_attack(self, attacker: Player, defender: Player):
        skill = attacker.active_creature.skills[0]  # Simplified for now
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name} on {defender.active_creature.display_name} for {damage} damage!")

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Base damage calculation
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def _get_type_effectiveness(self, attack_type: str, defender_type: str) -> float:
        if attack_type == "normal":
            return 1.0
        
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(attack_type, {}).get(defender_type, 1.0)

    def _has_available_creatures(self, player: Player) -> bool:
        return any(c.hp > 0 for c in player.creatures)
