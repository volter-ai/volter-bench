from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, create_from_game_database
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.turn_actions = []
        
    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.bot.display_name}'s {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap"""

    def reset_player_creatures(self, player):
        """Reset creatures to fresh state by recreating from prototypes"""
        fresh_creatures = []
        for creature in player.creatures:
            fresh_creature = create_from_game_database(creature.prototype_id, Creature)
            fresh_creatures.append(fresh_creature)
        player.creatures = fresh_creatures
        # Reset active creature to first creature
        player.active_creature = fresh_creatures[0]

    def run(self):
        self._show_text(self.player, "Battle Start!")
        try:
            while True:
                # Player turn
                if not self.handle_player_turn(self.player):
                    return
                
                # Bot turn
                if not self.handle_player_turn(self.bot):
                    return
                    
                # Resolve actions
                self.resolve_turn()
                
                # Check for battle end
                if self.check_battle_end():
                    self._quit_whole_game()
        finally:
            # Reset creature states when leaving scene for any reason
            self.reset_player_creatures(self.player)
            self.reset_player_creatures(self.bot)

    def handle_player_turn(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(current_player, [attack_button, swap_button])

            if choice == attack_button:
                # Show skills
                skills = [SelectThing(skill) for skill in current_player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(current_player, skills + [back_button])
                
                if skill_choice == back_button:
                    continue
                    
                self.turn_actions.append(("skill", current_player, skill_choice.thing))
                return True

            elif choice == swap_button:
                # Show available creatures
                available_creatures = [
                    SelectThing(creature) 
                    for creature in current_player.creatures 
                    if creature != current_player.active_creature and creature.hp > 0
                ]
                
                if not available_creatures:
                    self._show_text(current_player, "No creatures available to swap!")
                    continue
                    
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(current_player, available_creatures + [back_button])
                
                if creature_choice == back_button:
                    continue
                    
                self.turn_actions.append(("swap", current_player, creature_choice.thing))
                return True

    def resolve_turn(self):
        # Sort actions - swaps go first
        swaps = [action for action in self.turn_actions if action[0] == "swap"]
        skills = [action for action in self.turn_actions if action[0] == "skill"]
        
        # Execute swaps
        for action_type, player, creature in swaps:
            player.active_creature = creature
            self._show_text(self.player, f"{player.display_name} swapped to {creature.display_name}!")
            
        # Sort skills by speed
        if len(skills) == 2:
            attacker1, attacker2 = skills[0][1], skills[1][1]
            if attacker2.active_creature.speed > attacker1.active_creature.speed:
                skills.reverse()
            elif attacker2.active_creature.speed == attacker1.active_creature.speed:
                if random.random() < 0.5:
                    skills.reverse()
                    
        # Execute skills
        for action_type, attacker, skill in skills:
            defender = self.bot if attacker == self.player else self.player
            self.execute_skill(attacker, defender, skill)
            
        self.turn_actions = []

    def execute_skill(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Calculate type multiplier
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        
        # Calculate final damage
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage!")

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_battle_end(self):
        for player in [self.player, self.bot]:
            if player.active_creature.hp <= 0:
                # Try to swap
                available_creatures = [c for c in player.creatures if c.hp > 0]
                if not available_creatures:
                    winner = self.bot if player == self.player else self.player
                    self._show_text(self.player, f"{winner.display_name} wins!")
                    return True
                    
                choices = [SelectThing(c) for c in available_creatures]
                self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
                choice = self._wait_for_choice(player, choices)
                player.active_creature = choice.thing
                self._show_text(self.player, f"{player.display_name} sent out {choice.thing.display_name}!")
                
        return False
