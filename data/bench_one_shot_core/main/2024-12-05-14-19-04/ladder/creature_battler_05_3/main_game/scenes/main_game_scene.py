from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
from typing import List, Tuple, Optional
from main_game.models import Player, Creature, Skill

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
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = None
            while player_action is None:
                player_action = self.get_player_action(self.player)
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if bot_action is None:
                bot_action = ("attack", self.bot.active_creature.skills[0], self.bot.active_creature)
            
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            battle_result = self.check_battle_end()
            if battle_result is not None:
                if battle_result:
                    self._show_text(self.player, "You won the battle!")
                else:
                    self._show_text(self.player, "You lost the battle!")
                self._quit_whole_game()

    def get_player_action(self, player: Player) -> Optional[Tuple[str, Optional[Skill], Creature]]:
        action_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, [action_button, swap_button])
        
        if choice == action_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            skill_choice = self._wait_for_choice(player, skill_choices + [back_button])
            
            if skill_choice == back_button:
                return None
                
            return ("attack", skill_choice.thing, player.active_creature)
            
        else:
            # Show available creatures
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            
            if not creature_choices:
                self._show_text(player, "No creatures available to swap!")
                return None
                
            creature_choice = self._wait_for_choice(player, creature_choices + [back_button])
            
            if creature_choice == back_button:
                return None
                
            return ("swap", None, creature_choice.thing)

    def resolve_actions(self, player_action: Tuple[str, Optional[Skill], Creature], bot_action: Tuple[str, Optional[Skill], Creature]):
        actions = []
        if player_action is not None:
            actions.append(player_action)
        if bot_action is not None:
            actions.append(bot_action)
            
        # Handle swaps first
        for action in actions:
            if action[0] == "swap":
                if action == player_action:
                    self.player.active_creature = action[2]
                else:
                    self.bot.active_creature = action[2]
                    
        # Then handle attacks based on speed
        attack_actions = [a for a in actions if a[0] == "attack"]
        if len(attack_actions) == 2:
            # Sort by speed
            attack_actions.sort(key=lambda x: x[2].speed, reverse=True)
            
        for action in attack_actions:
            if action == player_action:
                attacker, defender = self.player.active_creature, self.bot.active_creature
            else:
                attacker, defender = self.bot.active_creature, self.player.active_creature
                
            self.execute_attack(action[1], attacker, defender)

    def execute_attack(self, skill: Skill, attacker: Creature, defender: Creature):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.hp = max(0, defender.hp - final_damage)
        
        # Show result
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"Dealt {final_damage} damage!")

    def get_type_multiplier(self, attack_type: str, defend_type: str) -> float:
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def check_battle_end(self) -> Optional[bool]:
        # Check if either player is out of usable creatures
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            return False  # Player lost
        elif not bot_has_creatures:
            return True  # Player won
            
        # Force swap if active creature is fainted
        if self.player.active_creature.hp <= 0:
            available = [c for c in self.player.creatures if c.hp > 0]
            if available:
                choices = [SelectThing(c) for c in available]
                choice = self._wait_for_choice(self.player, choices)
                self.player.active_creature = choice.thing
                
        if self.bot.active_creature.hp <= 0:
            available = [c for c in self.bot.creatures if c.hp > 0]
            if available:
                self.bot.active_creature = random.choice(available)
                
        return None  # Battle continues
