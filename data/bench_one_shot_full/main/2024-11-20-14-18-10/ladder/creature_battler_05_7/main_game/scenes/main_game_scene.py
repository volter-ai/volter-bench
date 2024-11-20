from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creatures by setting hp back to max_hp
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap (if available)"""

    def run(self):
        while True:
            # Check for battle end before getting actions
            if self.check_battle_end():
                return
                
            # Get and resolve actions
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            self.resolve_turn(player_action, bot_action)

    def get_player_action(self, player):
        while True:
            # Main action choices
            choices = [Button("Attack")]
            
            # Only offer swap if we have valid creatures to swap to
            valid_swap_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
            if valid_swap_creatures:
                choices.append(Button("Swap"))
            
            main_choice = self._wait_for_choice(player, choices)
            
            if main_choice.display_name == "Attack":
                # Show skills with Back option
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(Button("Back"))
                
                choice = self._wait_for_choice(player, skill_choices)
                if choice.display_name == "Back":
                    continue  # Go back to main choices
                return choice
            else:  # Must be swap
                # Show creatures with Back option
                creature_choices = [SelectThing(creature) for creature in valid_swap_creatures]
                creature_choices.append(Button("Back"))
                
                choice = self._wait_for_choice(player, creature_choices)
                if choice.display_name == "Back":
                    continue  # Go back to main choices
                return choice

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, type(self.player.creatures[0])):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, type(self.bot.creatures[0])):
            self.bot.active_creature = bot_action.thing

        # Then handle attacks
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Group actions by speed for proper randomization
        speed_groups = {}
        for actor, action in actions:
            if isinstance(action.thing, type(self.player.creatures[0].skills[0])):  # Only consider skill actions
                speed = actor.active_creature.speed
                if speed not in speed_groups:
                    speed_groups[speed] = []
                speed_groups[speed].append((actor, action))
        
        # Process actions in speed order, randomizing within same-speed groups
        ordered_actions = []
        for speed in sorted(speed_groups.keys(), reverse=True):
            group = speed_groups[speed]
            random.shuffle(group)  # Randomize order of same-speed actions
            ordered_actions.extend(group)
        
        # Execute actions in final order
        for actor, action in ordered_actions:
            self.execute_skill(actor, action)

    def execute_skill(self, attacker, skill):
        defender = self.bot if attacker == self.player else self.player
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"It dealt {final_damage} damage!")
        
        if defender.active_creature.hp == 0:
            self.handle_knockout(defender)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, player):
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        if valid_creatures:
            self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
            choices = [SelectThing(creature) for creature in valid_creatures]
            new_creature = self._wait_for_choice(player, choices).thing
            player.active_creature = new_creature

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
