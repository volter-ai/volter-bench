from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP" 
            for c in self.player.creatures
        )
        bot_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.hp} HP" 
            for c in self.bot.creatures
        )
        
        return f"""=== Battle ===
Your Active: {self.player.active_creature.display_name} ({self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP)
Foe's Active: {self.bot.active_creature.display_name} ({self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP)

Your Team:
{player_creatures_status}

Foe's Team:
{bot_creatures_status}

> Attack
> Swap (if available)
> Back (when in submenu)
"""

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

    def get_player_action(self, player):
        while True:
            # First check if there are available creatures to swap to
            available_creatures = [
                c for c in player.creatures 
                if c != player.active_creature and c.hp > 0
            ]

            # Build initial choice list
            choices = [Button("Attack")]
            if available_creatures:
                choices.append(Button("Swap"))

            initial_choice = self._wait_for_choice(player, choices)
            
            if initial_choice.display_name == "Attack":
                # Show skills with Back option
                back_button = Button("Back")
                skill_choices = [
                    SelectThing(skill) for skill in player.active_creature.skills
                ]
                skill_choices.append(back_button)
                
                choice = self._wait_for_choice(player, skill_choices)
                if choice == back_button:
                    continue
                return choice
            else:
                # Show creatures with Back option
                back_button = Button("Back")
                creature_choices = [
                    SelectThing(creature) for creature in available_creatures
                ]
                creature_choices.append(back_button)
                
                choice = self._wait_for_choice(player, creature_choices)
                if choice == back_button:
                    continue
                return choice

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, type(self.player.creatures[0])):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, type(self.bot.creatures[0])):
            self.bot.active_creature = bot_action.thing

        # Then handle attacks
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Determine action order based on speed with random tiebreaker
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            # Player goes first
            pass
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            # Bot goes first
            actions.reverse()
        else:
            # Speed tie - random order
            if random.choice([True, False]):
                actions.reverse()
        
        for attacker, action in actions:
            if isinstance(action.thing, type(self.player.active_creature.skills[0])):
                defender = self.bot if attacker == self.player else self.player
                self.execute_skill(action.thing, attacker, defender)

    def execute_skill(self, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = (
                attacker.active_creature.attack + 
                skill.base_damage - 
                defender.active_creature.defense
            )
        else:
            raw_damage = (
                skill.base_damage * 
                attacker.active_creature.sp_attack / 
                defender.active_creature.sp_defense
            )

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(
            skill.skill_type, 
            defender.active_creature.creature_type
        )
        
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)

        self._show_text(
            attacker,
            f"{attacker.active_creature.display_name} used {skill.display_name}!"
        )
        self._show_text(
            defender,
            f"{attacker.active_creature.display_name} used {skill.display_name}!"
        )

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
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if available_creatures:
            self._show_text(
                player,
                f"{player.active_creature.display_name} was knocked out! Choose a new creature!"
            )
            choice = self._wait_for_choice(
                player,
                [SelectThing(c) for c in available_creatures]
            )
            player.active_creature = choice.thing

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures or not bot_has_creatures:
            winner = self.player if player_has_creatures else self.bot
            self._show_text(self.player, 
                "You won!" if winner == self.player else "You lost!"
            )
            
            # Reset creatures
            for creature in self.player.creatures:
                creature.hp = creature.max_hp
            for creature in self.bot.creatures:
                creature.hp = creature.max_hp
                
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
