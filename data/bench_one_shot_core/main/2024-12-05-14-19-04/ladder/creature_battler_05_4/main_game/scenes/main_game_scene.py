from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        for p in [self.player, self.bot]:
            p.active_creature = p.creatures[0]
            for c in p.creatures:
                c.hp = c.max_hp

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

Available actions:
{'> Attack' if p_creature.hp > 0 else ''}
{'> Swap' if self.has_valid_swaps(self.player) else ''}"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if player_action is None:  # No valid actions - player lost
                self._show_text(self.player, f"{self.bot.display_name} wins!")
                self._quit_whole_game()
                return
                
            bot_action = self.get_player_action(self.bot)
            if bot_action is None:  # No valid actions - bot lost
                self._show_text(self.player, f"{self.player.display_name} wins!")
                self._quit_whole_game()
                return
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()
                return

    def has_valid_swaps(self, player):
        return any(c != player.active_creature and c.hp > 0 for c in player.creatures)

    def get_player_action(self, player):
        while True:
            main_choices = []
            
            # Only add Attack if creature isn't fainted
            if player.active_creature.hp > 0:
                main_choices.append(Button("Attack"))
                
            # Only add Swap if there are valid creatures to swap to
            if self.has_valid_swaps(player):
                main_choices.append(Button("Swap"))
                
            # If no choices available, player has lost
            if not main_choices:
                return None
                
            main_choice = self._wait_for_choice(player, main_choices)
            
            if main_choice.display_name == "Attack":
                choices = [SelectThing(skill) for skill in player.active_creature.skills]
                choices.append(Button("Back"))
                choice = self._wait_for_choice(player, choices)
                
                if choice.display_name == "Back":
                    continue
                return choice
                
            else:  # Swap
                valid_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
                choices = [SelectThing(creature) for creature in valid_creatures]
                choices.append(Button("Back"))
                choice = self._wait_for_choice(player, choices)
                
                if choice.display_name == "Back":
                    continue
                return choice

    def resolve_turn(self, p1_action, p2_action):
        # Handle swaps first
        for action, player in [(p1_action, self.player), (p2_action, self.bot)]:
            if isinstance(action.thing, Creature):
                player.active_creature = action.thing
                self._show_text(player, f"{player.display_name} swapped to {action.thing.display_name}!")

        # Then handle attacks with random speed tie resolution
        actions = [(p1_action, self.player, self.bot), (p2_action, self.bot, self.player)]
        # Sort by speed, using random tiebreaker for equal speeds
        actions.sort(key=lambda x: (x[1].active_creature.speed, random.random()), reverse=True)
        
        for action, attacker, defender in actions:
            if isinstance(action.thing, Creature):
                continue
                
            skill = action.thing
            damage = self.calculate_damage(skill, attacker.active_creature, defender.active_creature)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            
            self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
            self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")
            
            if defender.active_creature.hp == 0:
                self._show_text(defender, f"{defender.active_creature.display_name} fainted!")
                self.handle_faint(defender)

    def calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Calculate type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"water": 0.5, "leaf": 2.0},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def handle_faint(self, player):
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        if valid_creatures:
            choices = [SelectThing(c) for c in valid_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(player, f"Go, {choice.thing.display_name}!")

    def check_battle_end(self):
        for player in [self.player, self.bot]:
            if all(c.hp == 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                return True
        return False
