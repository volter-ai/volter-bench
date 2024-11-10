from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
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
            if player_action is None:  # Player chose to go back
                continue
                
            bot_action = self.get_player_action(self.bot)
            if bot_action is None:  # Should never happen for bot
                continue
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                action = self.get_attack_choice(player)
                if action:  # Only return if player didn't choose "Back"
                    return action
            else:
                action = self.get_swap_choice(player)
                if action:  # Only return if player didn't choose "Back"
                    return action

    def get_attack_choice(self, player):
        back_button = Button("Back")
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            return None
        return ("attack", choice.thing)

    def get_swap_choice(self, player):
        valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if not valid_creatures:
            return None
            
        back_button = Button("Back")
        choices = [SelectThing(creature) for creature in valid_creatures]
        choices.append(back_button)
        
        choice = self._wait_for_choice(player, choices)
        
        if choice == back_button:
            return None
        return ("swap", choice.thing)

    def resolve_turn(self, player_action, bot_action):
        if not player_action or not bot_action:
            return

        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]

        # Then handle attacks
        if player_action[0] == "attack" and bot_action[0] == "attack":
            # Determine order based on speed, with random tiebreaker
            player_speed = self.player.active_creature.speed
            bot_speed = self.bot.active_creature.speed
            
            if player_speed == bot_speed:
                # Random order for speed ties
                first = random.choice([self.player, self.bot])
            else:
                first = self.player if player_speed > bot_speed else self.bot
                
            second = self.bot if first == self.player else self.player
            first_action = player_action if first == self.player else bot_action
            second_action = bot_action if first == self.player else player_action
            
            self.execute_attack(first, second, first_action[1])
            if second.active_creature.hp > 0:
                self.execute_attack(second, first, second_action[1])

    def execute_attack(self, attacker, defender, skill):
        # Calculate raw damage
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
            self.handle_fainted_creature(defender)

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def handle_fainted_creature(self, player):
        self._show_text(player, f"{player.active_creature.display_name} fainted!")
        
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        if valid_creatures:
            choices = [SelectThing(creature) for creature in valid_creatures]
            player.active_creature = self._wait_for_choice(player, choices).thing

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
