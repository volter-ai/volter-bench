from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.turn_actions = []
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            self.handle_turn(self.player)
            
            # Bot turn
            self.handle_turn(self.bot)
            
            # Resolve actions
            self.resolve_actions()
            
            # Check for battle end
            if self.check_battle_end():
                # Reset creatures before leaving
                for creature in self.player.creatures:
                    creature.hp = creature.max_hp
                for creature in self.bot.creatures:
                    creature.hp = creature.max_hp
                    
                # Return to main menu
                self._transition_to_scene("MainMenuScene")
                return

    def handle_turn(self, current_player):
        if self.needs_forced_swap(current_player):
            self.handle_forced_swap(current_player)
            return

        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(current_player, [attack_button, swap_button])
        
        if choice == attack_button:
            self.handle_attack(current_player)
        else:
            self.handle_swap(current_player)

    def handle_attack(self, player):
        skills = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, skills + [back_button])
        
        if choice != back_button:
            self.turn_actions.append(("attack", player, choice.thing))

    def handle_swap(self, player):
        available_creatures = [
            SelectThing(creature) 
            for creature in player.creatures 
            if creature != player.active_creature and creature.hp > 0
        ]
        back_button = Button("Back")
        
        choice = self._wait_for_choice(player, available_creatures + [back_button])
        
        if choice != back_button:
            self.turn_actions.append(("swap", player, choice.thing))

    def resolve_actions(self):
        # Handle swaps first
        for action_type, player, thing in self.turn_actions:
            if action_type == "swap":
                player.active_creature = thing
                self._show_text(player, f"{player.display_name} swapped to {thing.display_name}!")

        # Then handle attacks
        attacks = [(p, t) for type_, p, t in self.turn_actions if type_ == "attack"]
        if len(attacks) == 2:
            # Sort by speed
            if attacks[0][0].active_creature.speed < attacks[1][0].active_creature.speed:
                attacks.reverse()
            elif attacks[0][0].active_creature.speed == attacks[1][0].active_creature.speed:
                if random.random() < 0.5:
                    attacks.reverse()

        for player, skill in attacks:
            target = self.bot if player == self.player else self.player
            self.execute_attack(player, target, skill)

        self.turn_actions.clear()

    def execute_attack(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {final_damage} damage!")

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def needs_forced_swap(self, player):
        return player.active_creature.hp <= 0

    def handle_forced_swap(self, player):
        available_creatures = [
            SelectThing(creature)
            for creature in player.creatures
            if creature.hp > 0
        ]
        
        if available_creatures:
            self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
            choice = self._wait_for_choice(player, available_creatures)
            player.active_creature = choice.thing
            self._show_text(player, f"{player.display_name} sent out {choice.thing.display_name}!")

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
