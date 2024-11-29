from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
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
                
        # Reset creatures
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = None
            
        self._transition_to_scene("MainMenuScene")

    def get_player_action(self, player):
        while True:
            attack = Button("Attack")
            swap = Button("Swap")
            choice = self._wait_for_choice(player, [attack, swap])
            
            if choice == attack:
                skills = [SelectThing(s) for s in player.active_creature.skills]
                back = Button("Back")
                skill_choice = self._wait_for_choice(player, skills + [back])
                if skill_choice != back:
                    return ("attack", skill_choice.thing)
            else:
                available = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                if available:
                    creatures = [SelectThing(c) for c in available]
                    back = Button("Back")
                    creature_choice = self._wait_for_choice(player, creatures + [back])
                    if creature_choice != back:
                        return ("swap", creature_choice.thing)

    def resolve_turn(self, p_action, b_action):
        # Handle swaps first
        if p_action[0] == "swap":
            self.player.active_creature = p_action[1]
        if b_action[0] == "swap":
            self.bot.active_creature = b_action[1]
            
        # Then handle attacks
        if p_action[0] == "attack" and b_action[0] == "attack":
            # Determine order
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                first, second = p_action, b_action
                first_player, second_player = self.player, self.bot
            elif self.player.active_creature.speed < self.bot.active_creature.speed:
                first, second = b_action, p_action
                first_player, second_player = self.bot, self.player
            else:
                if random.random() < 0.5:
                    first, second = p_action, b_action
                    first_player, second_player = self.player, self.bot
                else:
                    first, second = b_action, p_action
                    first_player, second_player = self.bot, self.player
                    
            # Execute attacks
            self.execute_attack(first[1], first_player, second_player)
            if second_player.active_creature.hp > 0:
                self.execute_attack(second[1], second_player, first_player)

    def execute_attack(self, skill, attacker, defender):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        factor = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(factor * raw_damage)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show result
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {final_damage} damage!")
        
        # Handle faint
        if defender.active_creature.hp == 0:
            self._show_text(defender, f"{defender.active_creature.display_name} was knocked out!")
            available = [c for c in defender.creatures if c.hp > 0]
            if available:
                creatures = [SelectThing(c) for c in available]
                choice = self._wait_for_choice(defender, creatures)
                defender.active_creature = choice.thing

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        elif skill_type == "fire":
            if creature_type == "leaf":
                return 2.0
            elif creature_type == "water":
                return 0.5
        elif skill_type == "water":
            if creature_type == "fire":
                return 2.0
            elif creature_type == "leaf":
                return 0.5
        elif skill_type == "leaf":
            if creature_type == "water":
                return 2.0
            elif creature_type == "fire":
                return 0.5
        return 1.0

    def check_battle_end(self):
        p_alive = any(c.hp > 0 for c in self.player.creatures)
        b_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_alive:
            self._show_text(self.player, "You lost!")
            return True
        elif not b_alive:
            self._show_text(self.player, "You won!")
            return True
            
        return False
