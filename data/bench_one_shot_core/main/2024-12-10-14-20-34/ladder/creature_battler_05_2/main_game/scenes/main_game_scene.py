from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        
        # Initialize creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

Your creatures: {[c.display_name for c in self.player.creatures]}
Foe's creatures: {[c.display_name for c in self.bot.creatures]}

> Attack
{"> Swap" if self.get_available_creatures(self.player) else ""}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Check for knocked out creatures and force swaps
            if self.player.active_creature.hp <= 0:
                if not self.handle_forced_swap(self.player):
                    self.end_battle(self.bot)
                    return
            if self.bot.active_creature.hp <= 0:
                if not self.handle_forced_swap(self.bot):
                    self.end_battle(self.player)
                    return

            # Get actions
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            winner = self.check_battle_end()
            if winner:
                self.end_battle(winner)
                return

    def end_battle(self, winner):
        # Show result
        if winner == self.player:
            self._show_text(self.player, "You won the battle!")
        else:
            self._show_text(self.player, "You lost the battle!")

        # Reset creature HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

        # Return to menu
        self._transition_to_scene("MainMenuScene")

    def get_available_creatures(self, current_player):
        return [c for c in current_player.creatures 
                if c != current_player.active_creature and c.hp > 0]

    def handle_forced_swap(self, current_player):
        available_creatures = self.get_available_creatures(current_player)
        if not available_creatures:
            return False
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(current_player, creature_choices)
        current_player.active_creature = choice.thing
        self._show_text(self.player, 
            f"{'You' if current_player == self.player else 'Foe'} was forced to swap to {choice.thing.display_name}!")
        return True

    def get_player_action(self, current_player):
        choices = [Button("Attack")]
        available_creatures = self.get_available_creatures(current_player)
        
        if available_creatures:
            choices.append(Button("Swap"))
            
        choice = self._wait_for_choice(current_player, choices)
        
        if choice.display_name == "Attack":
            # Show skills
            skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
            return self._wait_for_choice(current_player, skill_choices)
        else:
            # Show available creatures
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            return self._wait_for_choice(current_player, creature_choices)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
            self._show_text(self.player, f"You swapped to {player_action.thing.display_name}!")
            
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            self._show_text(self.player, f"Foe swapped to {bot_action.thing.display_name}!")

        # Then handle attacks
        first, second = self.determine_order(player_action, bot_action)
        self.execute_action(first)
        if isinstance(second.thing, Skill):  # Only execute second attack if it's a skill
            self.execute_action(second)

    def determine_order(self, player_action, bot_action):
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_action, bot_action
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return bot_action, player_action
        else:
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def execute_action(self, action):
        if isinstance(action.thing, Skill):
            attacker = self.player if action in self.player.active_creature.skills else self.bot
            defender = self.bot if attacker == self.player else self.player
            
            skill = action.thing
            damage = self.calculate_damage(skill, attacker.active_creature, defender.active_creature)
            
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name} for {damage} damage!")

    def calculate_damage(self, skill: Skill, attacker: Creature, defender: Creature) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        type_factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * type_factor)

    def get_type_effectiveness(self, attack_type: str, defend_type: str) -> float:
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            return self.bot
        elif not bot_has_creatures:
            return self.player
            
        return None
