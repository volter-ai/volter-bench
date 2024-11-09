from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Set initial active creatures
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
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            battle_result = self.check_battle_end()
            if battle_result:
                self._quit_whole_game()

    def get_player_action(self, player):
        if not player.active_creature or player.active_creature.hp <= 0:
            # Force swap if active creature is fainted
            swap_result = self.get_swap_choice(player)
            if not swap_result:  # No valid swaps available
                return None
            return ("swap", swap_result[1])

        while True:  # Loop to handle "Back" functionality
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                attack_result = self.get_attack_choice(player)
                if attack_result:
                    return attack_result
            else:
                swap_result = self.get_swap_choice(player)
                if swap_result:
                    return swap_result

    def get_attack_choice(self, player):
        if not player.active_creature or not player.active_creature.skills:
            return None
            
        # Add skills and Back button
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            return None
        return ("attack", choice.thing)

    def get_swap_choice(self, player):
        valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not valid_creatures:
            return None
            
        # Add creatures and Back button
        choices = [SelectThing(creature) for creature in valid_creatures]
        back_button = Button("Back")
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            return None
        return ("swap", choice.thing)

    def resolve_turn(self, player_action, bot_action):
        actions = []
        
        # Only process valid actions
        if player_action:
            actions.append((self.player, player_action))
        if bot_action:
            actions.append((self.bot, bot_action))

        # Handle swaps first
        for player, action in actions:
            if action[0] == "swap":
                player.active_creature = action[1]

        # Then handle attacks
        attack_actions = []
        for player, action in actions:
            if action[0] == "attack":
                opponent = self.bot if player == self.player else self.player
                if opponent.active_creature and opponent.active_creature.hp > 0:
                    # Add random factor for speed ties
                    random_factor = random.random()
                    attack_actions.append((player, opponent, action[1], random_factor))

        # Sort attacks by speed, using random factor for ties
        attack_actions.sort(key=lambda x: (x[0].active_creature.speed, x[3]), reverse=True)
        
        # Execute attacks (excluding random factor)
        for attacker, defender, skill, _ in attack_actions:
            if attacker.active_creature and attacker.active_creature.hp > 0:
                self.execute_skill(attacker.active_creature, defender.active_creature, skill)
                if defender.active_creature.hp <= 0:
                    self.handle_fainted_creature(defender)

    def execute_skill(self, attacker: Creature, defender: Creature, skill: Skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        
        final_damage = int(raw_damage * multiplier)
        defender.hp = max(0, defender.hp - final_damage)

        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"It dealt {final_damage} damage!")

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_fainted_creature(self, player):
        self._show_text(self.player, f"{player.active_creature.display_name} fainted!")
        
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        if valid_creatures:
            choices = [SelectThing(creature) for creature in valid_creatures]
            player.active_creature = self._wait_for_choice(player, choices).thing

    def check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
