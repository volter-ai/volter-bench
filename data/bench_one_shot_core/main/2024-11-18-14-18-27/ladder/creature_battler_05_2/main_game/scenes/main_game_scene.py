from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, create_from_game_database
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: HP {p_creature.hp}/{p_creature.max_hp}
Foe's {b_creature.display_name}: HP {b_creature.hp}/{b_creature.max_hp}

Your other creatures: {[c.display_name for c in self.player.creatures if c != p_creature and c.hp > 0]}
Foe's other creatures: {[c.display_name for c in self.bot.creatures if c != b_creature and c.hp > 0]}
"""

    def reset_player_creatures(self, player: Player):
        """Reset a player's creatures by recreating them from their prototype IDs"""
        original_creatures = player.creatures
        player.creatures = [
            create_from_game_database(creature.prototype_id, Creature)
            for creature in original_creatures
        ]
        player.active_creature = None

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player):
        attack = Button("Attack")
        swap = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack, swap])
        
        if choice == attack:
            skills = [SelectThing(skill) for skill in player.active_creature.skills]
            back = Button("Back")
            skill_choice = self._wait_for_choice(player, skills + [back])
            if skill_choice == back:
                return self.get_player_action(player)
            return ("attack", skill_choice.thing)
        else:
            available_creatures = [
                SelectThing(c) for c in player.creatures 
                if c != player.active_creature and c.hp > 0
            ]
            back = Button("Back")
            creature_choice = self._wait_for_choice(player, available_creatures + [back])
            if creature_choice == back:
                return self.get_player_action(player)
            return ("swap", creature_choice.thing)

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]

        # Then handle attacks
        actions = []
        if player_action[0] == "attack":
            actions.append((self.player, player_action[1]))
        if bot_action[0] == "attack":
            actions.append((self.bot, bot_action[1]))

        # Sort by speed
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        for attacker, skill in actions:
            defender = self.bot if attacker == self.player else self.player
            self.execute_skill(attacker.active_creature, defender.active_creature, skill)
            
            if defender.active_creature.hp <= 0:
                self.handle_knockout(defender)

    def execute_skill(self, attacker: Creature, defender: Creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        # Final damage
        final_damage = int(raw_damage * effectiveness)
        defender.hp = max(0, defender.hp - final_damage)

        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage!")

    def get_type_effectiveness(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if not available_creatures:
            winner = "You" if player == self.bot else "The opponent"
            self._show_text(self.player, f"{winner} won the battle!")
            # Reset both players' creatures before transitioning
            self.reset_player_creatures(self.player)
            self.reset_player_creatures(self.bot)
            self._transition_to_scene("MainMenuScene")
            return
            
        self._show_text(self.player, f"{player.active_creature.display_name} was knocked out!")
        choices = [SelectThing(c) for c in available_creatures]
        new_creature = self._wait_for_choice(player, choices).thing
        player.active_creature = new_creature

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        return not (player_alive and bot_alive)
