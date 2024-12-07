from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player):
        while True:
            choice = self._wait_for_choice(player, [
                Button("Attack"),
                Button("Swap"),
            ])

            if choice.display_name == "Attack":
                skills = [SelectThing(s, label=s.display_name) for s in player.active_creature.skills]
                skills.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skills)
                if not isinstance(skill_choice, Button):
                    return ("attack", skill_choice.thing)
            else:
                available_creatures = [
                    SelectThing(c, label=c.display_name) for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                available_creatures.append(Button("Back"))
                swap_choice = self._wait_for_choice(player, available_creatures)
                if not isinstance(swap_choice, Button):
                    return ("swap", swap_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]

        # Then handle attacks
        actions = []
        if player_action[0] == "attack":
            actions.append((self.player, self.bot, player_action[1], random.random()))  # Add random tiebreaker
        if bot_action[0] == "attack":
            actions.append((self.bot, self.player, bot_action[1], random.random()))  # Add random tiebreaker

        # Sort by speed, using random tiebreaker for equal speeds
        actions.sort(key=lambda x: (x[0].active_creature.speed, x[3]), reverse=True)
        
        # Execute actions without the tiebreaker value
        for attacker, defender, skill, _ in actions:
            damage = self.calculate_damage(
                attacker.active_creature,
                defender.active_creature,
                skill
            )
            defender.active_creature.hp -= damage
            self._show_text(
                self.player,
                f"{attacker.active_creature.display_name} used {skill.display_name} for {damage} damage!"
            )
            
            if defender.active_creature.hp <= 0:
                defender.active_creature.hp = 0
                self.handle_knockout(defender)

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Calculate type multiplier
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if not available_creatures:
            return
            
        self._show_text(
            player,
            f"{player.active_creature.display_name} was knocked out! Choose a new creature!"
        )
        
        swap_choice = self._wait_for_choice(
            player,
            [SelectThing(c, label=c.display_name) for c in available_creatures]
        )
        player.active_creature = swap_choice.thing

    def check_battle_end(self) -> bool:
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            winner = "You" if player_alive else "Bot"
            self._show_text(self.player, f"{winner} won the battle!")
            
            # Reset all creatures before leaving scene
            for p in [self.player, self.bot]:
                for c in p.creatures:
                    c.hp = c.max_hp
                p.active_creature = p.creatures[0]
            
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
