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

        # Reset creatures
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = None

        self._transition_to_scene("MainMenuScene")

    def get_player_action(self, player: Player) -> Tuple[str, Skill | Creature]:
        while True:
            choice = self._wait_for_choice(player, [
                Button("Attack"),
                Button("Swap")
            ])

            if choice.display_name == "Attack":
                skills = [SelectThing(s) for s in player.active_creature.skills]
                skills.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skills)
                
                if isinstance(skill_choice, Button):
                    continue
                    
                return ("attack", skill_choice.thing)
            else:
                available_creatures = [
                    c for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                if not available_creatures:
                    continue
                    
                creatures = [SelectThing(c) for c in available_creatures]
                creatures.append(Button("Back"))
                creature_choice = self._wait_for_choice(player, creatures)
                
                if isinstance(creature_choice, Button):
                    continue
                    
                return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action: Tuple[str, Skill | Creature], bot_action: Tuple[str, Skill | Creature]):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]

        # Then handle attacks
        if player_action[0] == "attack" and bot_action[0] == "attack":
            # Determine order
            first = self.player
            second = self.bot
            first_skill = player_action[1]
            second_skill = bot_action[1]
            
            if self.bot.active_creature.speed > self.player.active_creature.speed or \
               (self.bot.active_creature.speed == self.player.active_creature.speed and random.random() < 0.5):
                first, second = second, first
                first_skill, second_skill = second_skill, first_skill

            self.execute_attack(first, second, first_skill)
            if second.active_creature.hp > 0:
                self.execute_attack(second, first, second_skill)

    def execute_attack(self, attacker: Player, defender: Player, skill: Skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        factor = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        
        # Calculate final damage
        final_damage = int(raw_damage * factor)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)

        # Show damage text
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {final_damage} damage!")

        # Handle fainting
        if defender.active_creature.hp <= 0:
            self._show_text(defender, f"{defender.active_creature.display_name} fainted!")
            self.handle_faint(defender)

    def get_type_effectiveness(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def handle_faint(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            creatures = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, creatures)
            player.active_creature = choice.thing

    def check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
