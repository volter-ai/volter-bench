from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]
        
        # Reset creature HP
        for creature in self.player.creatures + self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if player_action is None:  # Player is still choosing
                continue
                
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player: Player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                action = self.get_attack_choice(player)
            else:
                action = self.get_swap_choice(player)
                
            if action is not None:  # Only return if we got a real action
                return action

    def get_attack_choice(self, player: Player):
        back_button = Button("Back")
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            return None
        return ("attack", choice.thing)

    def get_swap_choice(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not available_creatures:
            return self.get_attack_choice(player)
        
        back_button = Button("Back")
        choices = [SelectThing(creature) for creature in available_creatures]
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            return None
        return ("swap", choice.thing)

    def resolve_turn(self, player_action, bot_action):
        actions = [
            (self.player, player_action),
            (self.bot, bot_action)
        ]
        
        # Swaps go first
        for player, (action_type, action) in actions:
            if action_type == "swap":
                self._show_text(player, f"{player.display_name} swaps to {action.display_name}!")
                player.active_creature = action

        # Then attacks in speed order
        attacks = [(p, a) for p, (t, a) in actions if t == "attack"]
        if len(attacks) == 2:
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                ordered_attacks = attacks
            elif self.player.active_creature.speed < self.bot.active_creature.speed:
                ordered_attacks = attacks[::-1]
            else:
                ordered_attacks = random.sample(attacks, len(attacks))
        else:
            ordered_attacks = attacks

        for attacker, skill in ordered_attacks:
            defender = self.bot if attacker == self.player else self.player
            self.execute_attack(attacker, defender, skill)

    def execute_attack(self, attacker: Player, defender: Player, skill: Skill):
        self._show_text(attacker, f"{attacker.active_creature.display_name} uses {skill.display_name}!")
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        self._show_text(defender, f"{defender.active_creature.display_name} takes {final_damage} damage!")
        
        if defender.active_creature.hp == 0:
            self._show_text(defender, f"{defender.active_creature.display_name} is knocked out!")
            self.handle_knockout(defender)

    def get_type_effectiveness(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal" or creature_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)

    def handle_knockout(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            choices = [SelectThing(creature) for creature in available_creatures]
            self._show_text(player, "Choose next creature:")
            player.active_creature = self._wait_for_choice(player, choices).thing
            self._show_text(player, f"Go {player.active_creature.display_name}!")

    def check_battle_end(self) -> bool:
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            winner = self.player if player_alive else self.bot
            self._show_text(self.player, f"{winner.display_name} wins the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
