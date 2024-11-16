from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.reset_creatures()

    def reset_creatures(self):
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

    def __str__(self):
        p1 = self.player
        p2 = self.bot
        
        return f"""=== Battle ===
{p1.display_name}'s {p1.active_creature.display_name}: {p1.active_creature.hp}/{p1.active_creature.max_hp} HP
{p2.display_name}'s {p2.active_creature.display_name}: {p2.active_creature.hp}/{p2.active_creature.max_hp} HP

> Attack
{"> Swap" if self.get_available_creatures(p1) else ""}
"""

    def calculate_damage(self, attacker: Creature, defender: Creature, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": effectiveness = 2.0
            elif defender.creature_type == "water": effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": effectiveness = 2.0
            elif defender.creature_type == "leaf": effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": effectiveness = 2.0
            elif defender.creature_type == "fire": effectiveness = 0.5

        return int(raw_damage * effectiveness)

    def get_available_creatures(self, player: Player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_knocked_out(self, player: Player):
        available = self.get_available_creatures(player)
        if not available:
            return False
        
        choices = [SelectThing(c) for c in available]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return True

    def get_player_action(self, player: Player):
        while True:
            # Main action choices
            choices = [Button("Attack")]
            if self.get_available_creatures(player):
                choices.append(Button("Swap"))
            
            choice = self._wait_for_choice(player, choices)

            if choice.display_name == "Attack":
                # Show skills with Back option
                choices = [SelectThing(s) for s in player.active_creature.skills]
                choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, choices)
                
                if skill_choice.display_name == "Back":
                    continue
                return ("attack", skill_choice.thing)
            else:
                # Show creatures with Back option
                choices = [SelectThing(c) for c in self.get_available_creatures(player)]
                choices.append(Button("Back"))
                creature_choice = self._wait_for_choice(player, choices)
                
                if creature_choice.display_name == "Back":
                    continue
                return ("swap", creature_choice.thing)

    def run(self):
        while True:
            # Player Choice Phase
            player_action = self.get_player_action(self.player)
            
            # Foe Choice Phase
            bot_action = self.get_player_action(self.bot)  # Bot uses same choice system

            # Resolution Phase
            actions = [(self.player, player_action), (self.bot, bot_action)]
            
            # Sort by speed and randomize ties
            actions.sort(key=lambda x: (
                x[1][0] != "swap",  # Swaps always go first
                -x[0].active_creature.speed if x[1][0] != "swap" else 0,
                random.random()  # Random tiebreaker for equal speeds
            ))

            # Execute actions
            for player, (action_type, target) in actions:
                opponent = self.bot if player == self.player else self.player
                
                if action_type == "swap":
                    player.active_creature = target
                    self._show_text(player, f"{player.display_name} swapped to {target.display_name}!")
                else:
                    damage = self.calculate_damage(player.active_creature, opponent.active_creature, target)
                    opponent.active_creature.hp -= damage
                    self._show_text(player, f"{player.active_creature.display_name} used {target.display_name} for {damage} damage!")

                    if opponent.active_creature.hp <= 0:
                        opponent.active_creature.hp = 0
                        if not self.handle_knocked_out(opponent):
                            self._show_text(self.player, f"{player.display_name} wins!")
                            self.reset_creatures()
                            self._quit_whole_game()
