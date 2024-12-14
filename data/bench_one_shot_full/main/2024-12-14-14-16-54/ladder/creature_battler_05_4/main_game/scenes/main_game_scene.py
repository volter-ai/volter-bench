from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
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

Your other creatures: {[c.display_name for c in self.player.creatures if c != p_creature and c.hp > 0]}
Foe's other creatures: {[c.display_name for c in self.bot.creatures if c != b_creature and c.hp > 0]}
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
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
            choice = self._wait_for_choice(player, [
                Button("Attack"),
                Button("Swap"),
            ])

            if isinstance(choice, Button) and choice.display_name == "Attack":
                skills = [SelectThing(s) for s in player.active_creature.skills]
                skills.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skills)
                
                if isinstance(skill_choice, Button):
                    continue  # Back button pressed
                else:
                    return ("attack", skill_choice.thing)
            else:
                available_creatures = [
                    SelectThing(c) for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                available_creatures.append(Button("Back"))
                swap_choice = self._wait_for_choice(player, available_creatures)
                
                if isinstance(swap_choice, Button):
                    continue  # Back button pressed
                else:
                    return ("swap", swap_choice.thing)

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        for action, player in [(player_action, self.player), (bot_action, self.bot)]:
            if action[0] == "swap":
                old_creature = player.active_creature
                player.active_creature = action[1]
                self._show_text(self.player, f"{player.display_name} swapped {old_creature.display_name} for {action[1].display_name}!")

        # Then handle attacks
        actions = [(player_action, self.player, self.bot), (bot_action, self.bot, self.player)]
        actions.sort(key=lambda x: x[1].active_creature.speed, reverse=True)
        
        for action, attacker, defender in actions:
            if action[0] == "attack":
                damage = self.calculate_damage(action[1], attacker.active_creature, defender.active_creature)
                defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
                self._show_text(self.player, 
                    f"{attacker.display_name}'s {attacker.active_creature.display_name} used {action[1].display_name} "
                    f"on {defender.display_name}'s {defender.active_creature.display_name} for {damage} damage!")
                
                if defender.active_creature.hp == 0:
                    self.handle_knockout(defender)

    def calculate_damage(self, skill, attacker, defender):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Calculate type multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": multiplier = 2.0
            elif defender.creature_type == "water": multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": multiplier = 2.0
            elif defender.creature_type == "leaf": multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": multiplier = 2.0
            elif defender.creature_type == "fire": multiplier = 0.5
            
        return int(raw_damage * multiplier)

    def handle_knockout(self, player):
        self._show_text(self.player, f"{player.display_name}'s {player.active_creature.display_name} was knocked out!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            swap_choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, swap_choices)
            player.active_creature = choice.thing
            self._show_text(self.player, f"{player.display_name} sent out {choice.thing.display_name}!")

    def check_battle_end(self):
        for player in [self.player, self.bot]:
            if not any(c.hp > 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                return True
        return False
