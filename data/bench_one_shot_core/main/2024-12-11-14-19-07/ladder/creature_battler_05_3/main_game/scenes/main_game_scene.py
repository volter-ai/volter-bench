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
> Swap
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
                Button("Swap")
            ])

            if choice.display_name == "Attack":
                skills = [SelectThing(s) for s in player.active_creature.skills]
                skills.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skills)
                
                # Check if it's a Button (Back) or SelectThing
                if isinstance(skill_choice, SelectThing):
                    return ("attack", skill_choice.thing)
            else:
                available_creatures = [
                    SelectThing(c) for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                available_creatures.append(Button("Back"))
                creature_choice = self._wait_for_choice(player, available_creatures)
                
                # Check if it's a Button (Back) or SelectThing
                if isinstance(creature_choice, SelectThing):
                    return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Handle swaps first
        for player, action in actions:
            if action[0] == "swap":
                player.active_creature = action[1]
                self._show_text(player, f"{player.display_name} swapped to {action[1].display_name}!")

        # Then handle attacks
        random.shuffle(actions)  # For speed ties
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        for player, action in actions:
            if action[0] == "attack":
                skill = action[1]
                attacker = player.active_creature
                defender = self.bot.active_creature if player == self.player else self.player.active_creature
                
                # Calculate damage
                if skill.is_physical:
                    raw_damage = attacker.attack + skill.base_damage - defender.defense
                else:
                    raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
                
                # Type effectiveness
                effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
                final_damage = int(raw_damage * effectiveness)
                
                defender.hp = max(0, defender.hp - final_damage)
                self._show_text(player, f"{attacker.display_name} used {skill.display_name}!")
                self._show_text(player, f"Dealt {final_damage} damage!")
                
                if defender.hp == 0:
                    self.handle_knockout(self.bot if player == self.player else self.player)

    def get_type_effectiveness(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, player):
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        available_creatures = [c for c in player.creatures if c.hp > 0]
        
        if available_creatures:
            choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(player, f"{player.display_name} sent out {choice.thing.display_name}!")

    def check_battle_end(self):
        for p in [self.player, self.bot]:
            if not any(c.hp > 0 for c in p.creatures):
                winner = self.bot if p == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                return True
        return False
