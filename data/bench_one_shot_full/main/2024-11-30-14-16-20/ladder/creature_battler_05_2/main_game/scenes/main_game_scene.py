from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.initialize_battle()

    def initialize_battle(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP"""

    def run(self):
        while True:
            if self.check_battle_end():
                self._quit_whole_game()
                return
                
            player_action = self.get_player_action(self.player)
            bot_action = self.get_bot_action()
            
            self.resolve_turn(player_action, bot_action)

    def get_player_action(self, player):
        while True:
            # Get available creatures for swapping
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            
            # Build main menu choices
            choices = []
            if player.active_creature.hp > 0:
                choices.append(Button("Attack"))
            if available_creatures:
                choices.append(Button("Swap"))
            
            main_choice = self._wait_for_choice(player, choices)
            
            if main_choice.display_name == "Attack":
                # Show skills with Back option
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(Button("Back"))
                
                choice = self._wait_for_choice(player, skill_choices)
                if choice.display_name == "Back":
                    continue  # Go back to main menu
                return choice
            else:
                # Show available creatures with Back option
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choices.append(Button("Back"))
                
                choice = self._wait_for_choice(player, creature_choices)
                if choice.display_name == "Back":
                    continue  # Go back to main menu
                return choice

    def get_bot_action(self):
        # Get available creatures for swapping
        available_creatures = [c for c in self.bot.creatures if c.hp > 0 and c != self.bot.active_creature]
        
        # Build possible actions
        possible_actions = []
        
        # Add attack option if active creature has HP
        if self.bot.active_creature.hp > 0:
            for skill in self.bot.active_creature.skills:
                possible_actions.append(SelectThing(skill))
                
        # Add swap options if there are available creatures
        for creature in available_creatures:
            possible_actions.append(SelectThing(creature))
            
        # Randomly choose an action
        return random.choice(possible_actions)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing

        # Determine order for attacks
        first = self.player
        second = self.bot
        if self.bot.active_creature.speed > self.player.active_creature.speed:
            first, second = second, first
        elif self.bot.active_creature.speed == self.player.active_creature.speed:
            if random.random() < 0.5:
                first, second = second, first

        # Execute attacks
        for attacker, action in [(first, player_action if first == self.player else bot_action),
                               (second, bot_action if second == self.bot else player_action)]:
            if isinstance(action.thing, Creature):
                continue
                
            skill = action.thing
            defender = self.bot if attacker == self.player else self.player
            
            damage = self.calculate_damage(skill, attacker.active_creature, defender.active_creature)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            
            self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
            self._show_text(attacker, f"Dealt {damage} damage!")

            if defender.active_creature.hp == 0:
                self.handle_fainted_creature(defender)

    def calculate_damage(self, skill, attacker, defender):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_fainted_creature(self, player):
        self._show_text(player, f"{player.active_creature.display_name} fainted!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        new_creature = self._wait_for_choice(player, creature_choices).thing
        player.active_creature = new_creature

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures or not bot_has_creatures:
            winner = self.player if player_has_creatures else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            return True
            
        return False
