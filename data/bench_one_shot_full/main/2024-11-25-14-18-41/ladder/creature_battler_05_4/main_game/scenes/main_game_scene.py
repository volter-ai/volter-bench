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
            f"{c.display_name}: {c.hp}/{c.max_hp} HP" 
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
"""

    def run(self):
        game_running = True
        while game_running:
            # Check for battle end before each turn
            if self.check_battle_end():
                self._quit_whole_game()
                game_running = False
                continue
                
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:  # No valid actions available
                self._show_text(self.player, "You lost the battle!")
                self._quit_whole_game()
                game_running = False
                continue
                
            bot_action = self.get_player_action(self.bot)
            if not bot_action:  # No valid actions available
                self._show_text(self.player, "You won the battle!")
                self._quit_whole_game()
                game_running = False
                continue
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)

    def get_available_creatures(self, player):
        return [c for c in player.creatures if c != player.active_creature and c.hp > 0]

    def get_player_action(self, player):
        choices = []
        
        # Only offer Attack if the active creature has HP
        if player.active_creature.hp > 0:
            choices.append(Button("Attack"))
            
        # Only offer Swap if there are creatures available to swap to
        available_creatures = self.get_available_creatures(player)
        if available_creatures:
            choices.append(Button("Swap"))
            
        # If no choices available, player has lost
        if not choices:
            return None
            
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            return self._wait_for_choice(player, [
                SelectThing(skill) for skill in player.active_creature.skills
            ])
        else:  # Swap
            return self._wait_for_choice(player, [
                SelectThing(creature) for creature in available_creatures
            ])

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, type(self.player.creatures[0])):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action.thing, type(self.bot.creatures[0])):
            self.bot.active_creature = bot_action.thing

        # Then handle attacks
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Sort by speed for attack order
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        for attacker, action in actions:
            if isinstance(action.thing, type(self.player.creatures[0].skills[0])):
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
        available_creatures = self.get_available_creatures(player)
        
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
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
