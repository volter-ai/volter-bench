from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        
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

Your creatures: {[c.display_name for c in self.player.creatures]}
Foe's creatures: {[c.display_name for c in self.bot.creatures]}
"""

    def run(self):
        while True:
            # Show current state
            self._show_text(self.player, str(self))
            
            # Get player action
            player_action = self.get_player_action(self.player)
            if not player_action:
                self._quit_whole_game()
                return
                
            # Get bot action
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                self._quit_whole_game()
                return
                
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # After showing the winner, ask player if they want to play again
                play_again = Button("Play Again")
                quit_game = Button("Quit")
                choice = self._wait_for_choice(self.player, [play_again, quit_game])
                
                if choice == play_again:
                    self._transition_to_scene("MainGameScene")
                else:
                    self._quit_whole_game()
                return

    def get_player_action(self, player):
        # First level menu
        attack = Button("Attack")
        swap = Button("Swap")
        choice = self._wait_for_choice(player, [attack, swap])
        
        if choice == attack:
            # Show skills
            skills = [SelectThing(s) for s in player.active_creature.skills]
            return self._wait_for_choice(player, skills)
        else:
            # Show available creatures
            available = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
            if not available:
                return None
            creatures = [SelectThing(c) for c in available]
            return self._wait_for_choice(player, creatures)

    def resolve_actions(self, p_action, b_action):
        # Determine order
        first = self.player
        second = self.bot
        first_action = p_action
        second_action = b_action
        
        if isinstance(p_action.thing, Creature) and isinstance(b_action.thing, Creature):
            # Both swapping
            self.execute_swap(self.player, p_action.thing)
            self.execute_swap(self.bot, b_action.thing)
            return
            
        if isinstance(b_action.thing, Creature):
            # Bot swapping
            self.execute_swap(self.bot, b_action.thing)
            self.execute_attack(self.player, p_action.thing, self.bot)
            return
            
        if isinstance(p_action.thing, Creature):
            # Player swapping
            self.execute_swap(self.player, p_action.thing)
            self.execute_attack(self.bot, b_action.thing, self.player)
            return
            
        # Both attacking - check speed
        if self.bot.active_creature.speed > self.player.active_creature.speed:
            first, second = self.bot, self.player
            first_action, second_action = b_action, p_action
        elif self.bot.active_creature.speed < self.player.active_creature.speed:
            first, second = self.player, self.bot
            first_action, second_action = p_action, b_action
        else:
            # Random on speed tie
            if random.random() < 0.5:
                first, second = self.bot, self.player
                first_action, second_action = b_action, p_action
                
        self.execute_attack(first, first_action.thing, second)
        if second.active_creature.hp > 0:
            self.execute_attack(second, second_action.thing, first)

    def execute_attack(self, attacker, skill, defender):
        # Calculate damage
        raw_damage = 0
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Type effectiveness
        factor = self.get_type_factor(skill.skill_type, defender.active_creature.creature_type)
        
        # Apply damage
        final_damage = int(raw_damage * factor)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}")
        
        # Force swap if knocked out
        if defender.active_creature.hp == 0:
            self.force_swap(defender)

    def execute_swap(self, player, new_creature):
        old = player.active_creature
        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} swapped {old.display_name} for {new_creature.display_name}!")

    def force_swap(self, player):
        available = [c for c in player.creatures if c.hp > 0]
        if not available:
            return False
            
        if len(available) == 1:
            self.execute_swap(player, available[0])
        else:
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(player, choices)
            self.execute_swap(player, choice.thing)
        return True

    def check_battle_end(self):
        p_alive = any(c.hp > 0 for c in self.player.creatures)
        b_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_alive or not b_alive:
            winner = self.player if p_alive else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            return True
        return False

    def get_type_factor(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)
