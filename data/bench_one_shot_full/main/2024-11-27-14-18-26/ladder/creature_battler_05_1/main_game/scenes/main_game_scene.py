from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.initialize_creatures()

    def initialize_creatures(self):
        for p in [self.player, self.bot]:
            p.active_creature = p.creatures[0]
            for c in p.creatures:
                c.hp = c.max_hp

    def __str__(self):
        p1 = self.player
        p2 = self.bot
        
        return f"""=== Battle ===
{p1.display_name}'s {p1.active_creature.display_name}: {p1.active_creature.hp}/{p1.active_creature.max_hp} HP
{p2.display_name}'s {p2.active_creature.display_name}: {p2.active_creature.hp}/{p2.active_creature.max_hp} HP

Actions:
> Attack
> Swap"""

    def run(self):
        while True:
            # Player Choice Phase
            self._show_text(self.player, "=== Player Choice Phase ===")
            player_action = self.get_player_choice_phase(self.player)
            if player_action is None:
                self.handle_no_valid_actions(self.player)
                break

            # Foe Choice Phase
            self._show_text(self.player, "=== Foe Choice Phase ===")
            bot_action = self.get_player_choice_phase(self.bot)
            if bot_action is None:
                self.handle_no_valid_actions(self.bot)
                break
            
            # Resolution Phase
            self._show_text(self.player, "=== Resolution Phase ===")
            self.resolve_turn(player_action, bot_action)
            
            if self.check_battle_end():
                break

    def get_player_choice_phase(self, player):
        while True:
            # Main menu choices
            choices = []
            if player.active_creature and player.active_creature.skills:
                choices.append(Button("Attack"))
            
            available_creatures = [c for c in player.creatures 
                                 if c != player.active_creature and c.hp > 0]
            if available_creatures:
                choices.append(Button("Swap"))
                
            if not choices:
                return None
                
            main_choice = self._wait_for_choice(player, choices)
            
            # Sub-menu choices with Back option
            if isinstance(main_choice, Button) and main_choice.display_name == "Attack":
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(Button("Back"))
                
                choice = self._wait_for_choice(player, skill_choices)
                if isinstance(choice, Button) and choice.display_name == "Back":
                    continue
                return choice
                
            else:  # Swap
                swap_choices = [SelectThing(creature) for creature in available_creatures]
                swap_choices.append(Button("Back"))
                
                choice = self._wait_for_choice(player, swap_choices)
                if isinstance(choice, Button) and choice.display_name == "Back":
                    continue
                return choice

    def handle_no_valid_actions(self, player):
        self._show_text(player, f"{player.display_name} has no valid actions left!")
        winner = self.bot if player == self.player else self.player
        self._show_text(self.player, f"{winner.display_name} wins the battle!")
        self.reset_creature_state()
        self._transition_to_scene("MainMenuScene")

    def reset_creature_state(self):
        """Reset all creatures to their original state"""
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

    def resolve_turn(self, p1_action, p2_action):
        # Handle swaps first
        for action, player in [(p1_action, self.player), (p2_action, self.bot)]:
            if isinstance(action.thing, Creature):
                player.active_creature = action.thing
                self._show_text(player, f"{player.display_name} swapped to {action.thing.display_name}!")

        # Then handle attacks
        actions = [(p1_action, self.player, self.bot), 
                  (p2_action, self.bot, self.player)]
        
        # Sort by speed
        actions.sort(key=lambda x: x[1].active_creature.speed, reverse=True)
        
        for action, attacker, defender in actions:
            if isinstance(action.thing, Creature):
                continue
                
            skill = action.thing
            damage = self.calculate_damage(skill, attacker.active_creature, 
                                        defender.active_creature)
            
            defender.active_creature.hp -= damage
            defender.active_creature.hp = max(0, defender.active_creature.hp)
            
            self._show_text(attacker, 
                f"{attacker.active_creature.display_name} used {skill.display_name}!")
            self._show_text(defender,
                f"{defender.active_creature.display_name} took {damage} damage!")
            
            if defender.active_creature.hp == 0:
                self.handle_knockout(defender)

    def calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, 
                                                 defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)

    def handle_knockout(self, player):
        self._show_text(player, 
            f"{player.active_creature.display_name} was knocked out!")
            
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if not available_creatures:
            return
            
        new_creature = self._wait_for_choice(player,
            [SelectThing(c) for c in available_creatures]).thing
            
        player.active_creature = new_creature
        self._show_text(player,
            f"{player.display_name} sent out {new_creature.display_name}!")

    def check_battle_end(self):
        for player in [self.player, self.bot]:
            if not any(c.hp > 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player,
                    f"{winner.display_name} wins the battle!")
                self.reset_creature_state()
                self._transition_to_scene("MainMenuScene")
                return True
        return False
