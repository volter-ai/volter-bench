from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
from typing import List, Tuple
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp  # Reset HP directly instead of using a method
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
            if not player_action:
                continue
                
            # Bot turn
            bot_action = self.get_bot_action()
            
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player: Player) -> Tuple[str, Skill | Creature]:
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            choices = [SelectThing(s) for s in player.active_creature.skills]
            choices.append(Button("Back"))
            choice = self._wait_for_choice(player, choices)
            if isinstance(choice, Button):
                return None
            return ("attack", choice.thing)
            
        elif choice == swap_button:
            available = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
            if not available:
                self._show_text(player, "No creatures available to swap!")
                return None
            choices = [SelectThing(c) for c in available]
            choices.append(Button("Back"))
            choice = self._wait_for_choice(player, choices)
            if isinstance(choice, Button):
                return None
            return ("swap", choice.thing)

    def get_bot_action(self) -> Tuple[str, Skill | Creature]:
        # Simple bot AI - randomly attack or swap
        if random.random() < 0.8:  # 80% chance to attack
            skill = random.choice(self.bot.active_creature.skills)
            return ("attack", skill)
        else:
            available = [c for c in self.bot.creatures if c != self.bot.active_creature and c.hp > 0]
            if available:
                return ("swap", random.choice(available))
            return ("attack", random.choice(self.bot.active_creature.skills))

    def resolve_actions(self, player_action: Tuple[str, Skill | Creature], bot_action: Tuple[str, Skill | Creature]):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            
        # Then handle attacks
        actions = []
        if player_action[0] == "attack":
            actions.append((self.player, self.bot, player_action[1]))
        if bot_action[0] == "attack":
            actions.append((self.bot, self.player, bot_action[1]))
            
        # Sort by speed
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        # Execute attacks
        for attacker, defender, skill in actions:
            self.execute_skill(attacker.active_creature, defender.active_creature, skill)
            if defender.active_creature.hp <= 0:
                self.handle_knockout(defender)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        factor = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * factor)
        
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}! Dealt {final_damage} damage!")

    def get_type_effectiveness(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, player: Player):
        self._show_text(self.player, f"{player.active_creature.display_name} was knocked out!")
        available = [c for c in player.creatures if c.hp > 0]
        
        if not available:
            return
            
        if player == self.player:
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
        else:
            player.active_creature = random.choice(available)

    def check_battle_end(self) -> bool:
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            winner = "You" if player_alive else "Bot"
            self._show_text(self.player, f"{winner} won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
