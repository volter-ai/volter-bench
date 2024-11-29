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
            if self.check_battle_end():
                break
                
            # Player turn
            player_action = self.get_player_action(self.player)
            if self.check_battle_end():
                break
                
            bot_action = self.get_player_action(self.bot)
            if self.check_battle_end():
                break
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
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
            # First check if we can only attack
            available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
            
            if not available_creatures:
                # If no swaps available, force attack
                skills = [SelectThing(s) for s in player.active_creature.skills]
                return self._wait_for_choice(player, skills)
            
            # Otherwise show both options
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Show skills with back option
                skills = [SelectThing(s) for s in player.active_creature.skills]
                back_button = Button("Back")
                
                skill_choice = self._wait_for_choice(player, skills + [back_button])
                if skill_choice == back_button:
                    continue  # Go back to main menu
                return skill_choice
            else:
                # Show creatures with back option
                creatures = [SelectThing(c) for c in available_creatures]
                back_button = Button("Back")
                
                creature_choice = self._wait_for_choice(player, creatures + [back_button])
                if creature_choice == back_button:
                    continue  # Go back to main menu
                return creature_choice

    def resolve_turn(self, p_action, b_action):
        # Handle swaps first
        if isinstance(p_action.thing, Creature):
            self.player.active_creature = p_action.thing
        if isinstance(b_action.thing, Creature):
            self.bot.active_creature = b_action.thing
            
        # Then handle attacks
        actions = [(self.player, p_action), (self.bot, b_action)]
        
        # Determine action order based on speed
        p_speed = self.player.active_creature.speed
        b_speed = self.bot.active_creature.speed
        
        if p_speed == b_speed:
            # If speeds are equal, randomly choose order
            random.shuffle(actions)
        else:
            # Otherwise sort by speed
            actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        for player, action in actions:
            if isinstance(action.thing, Creature):
                continue
                
            skill = action.thing
            target = self.bot if player == self.player else self.player
            
            damage = self.calculate_damage(skill, player.active_creature, target.active_creature)
            target.active_creature.hp = max(0, target.active_creature.hp - damage)
            
            self._show_text(player, f"{player.active_creature.display_name} used {skill.display_name}!")
            self._show_text(player, f"Dealt {damage} damage!")
            
            if target.active_creature.hp == 0:
                if not self.handle_knockout(target):
                    return # Battle is over

    def calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw = attacker.attack + skill.base_damage - defender.defense
        else:
            raw = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw * effectiveness)

    def get_type_effectiveness(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def handle_knockout(self, player):
        """Returns True if the battle should continue, False if it should end"""
        available = [c for c in player.creatures if c.hp > 0]
        if not available:
            winner = self.player if player == self.bot else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            return False
            
        creatures = [SelectThing(c) for c in available]
        new_creature = self._wait_for_choice(player, creatures).thing
        player.active_creature = new_creature
        return True

    def check_battle_end(self):
        for p in [self.player, self.bot]:
            if not any(c.hp > 0 for c in p.creatures):
                return True
        return False
