from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.reset_creatures()

    def reset_creatures(self):
        # Reset all creatures to max HP
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
> Swap
"""

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Calculate type multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf":
                multiplier = 2.0
            elif defender_creature.creature_type == "water":
                multiplier = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire":
                multiplier = 2.0
            elif defender_creature.creature_type == "leaf":
                multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water":
                multiplier = 2.0
            elif defender_creature.creature_type == "fire":
                multiplier = 0.5

        return int(raw_damage * multiplier)

    def get_available_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_fainted_creature(self, player):
        available = self.get_available_creatures(player)
        if not available:
            return False
        
        choices = [SelectThing(creature) for creature in available]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return True

    def get_player_action(self):
        # First check if we can do anything
        if self.player.active_creature.hp <= 0 and not self.get_available_creatures(self.player):
            return None

        # If active creature is fainted, must swap
        if self.player.active_creature.hp <= 0:
            available = self.get_available_creatures(self.player)
            if available:
                choices = [SelectThing(creature) for creature in available]
                choice = self._wait_for_choice(self.player, choices)
                return ("swap", choice.thing)
            return None

        # Normal turn - can attack or swap
        while True:  # Main choice loop
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            available_creatures = self.get_available_creatures(self.player)
            choices = [attack_button]
            if available_creatures:
                choices.append(swap_button)
                
            choice = self._wait_for_choice(self.player, choices)

            if choice == attack_button:
                # Attack submenu with Back option
                skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                back_button = Button("Back")
                skill_choices.append(back_button)
                
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                if skill_choice == back_button:
                    continue  # Go back to main choice
                return ("attack", skill_choice.thing)
            else:
                # Swap submenu with Back option
                creature_choices = [SelectThing(c) for c in available_creatures]
                back_button = Button("Back")
                creature_choices.append(back_button)
                
                creature_choice = self._wait_for_choice(self.player, creature_choices)
                if creature_choice == back_button:
                    continue  # Go back to main choice
                return ("swap", creature_choice.thing)

    def run(self):
        while True:
            # Get player action
            player_action = self.get_player_action()
            if player_action is None:
                self._show_text(self.player, "You lost!")
                break

            # Bot turn
            bot_action = ("attack", random.choice(self.bot.active_creature.skills))

            # Resolution phase
            if player_action[0] == "swap":
                self.player.active_creature = player_action[1]
                self._show_text(self.player, f"You switched to {player_action[1].display_name}!")
                
                # Bot attacks the new creature
                damage = self.calculate_damage(self.bot.active_creature, self.player.active_creature, bot_action[1])
                self.player.active_creature.hp -= damage
                self._show_text(self.player, f"Foe's {self.bot.active_creature.display_name} used {bot_action[1].display_name}!")
                self._show_text(self.player, f"Your {self.player.active_creature.display_name} took {damage} damage!")

            else:
                # Determine order
                first = self.player
                second = self.bot
                first_action = player_action
                second_action = bot_action
                
                if self.bot.active_creature.speed > self.player.active_creature.speed:
                    first = self.bot
                    second = self.player
                    first_action = bot_action
                    second_action = player_action
                elif self.bot.active_creature.speed == self.player.active_creature.speed:
                    if random.random() < 0.5:
                        first = self.bot
                        second = self.player
                        first_action = bot_action
                        second_action = player_action

                # Execute actions in order
                for attacker, defender, action in [(first, second, first_action), (second, first, second_action)]:
                    if defender.active_creature.hp <= 0:
                        continue
                        
                    damage = self.calculate_damage(attacker.active_creature, defender.active_creature, action[1])
                    defender.active_creature.hp -= damage
                    
                    owner_text = "Your" if attacker == self.player else "Foe's"
                    self._show_text(self.player, 
                        f"{owner_text} {attacker.active_creature.display_name} used {action[1].display_name}!")
                    
                    target_text = "Your" if defender == self.player else "Foe's"
                    self._show_text(self.player,
                        f"{target_text} {defender.active_creature.display_name} took {damage} damage!")

            # Check for fainted creatures
            if self.player.active_creature.hp <= 0:
                if not self.handle_fainted_creature(self.player):
                    self._show_text(self.player, "You lost!")
                    break
            
            if self.bot.active_creature.hp <= 0:
                if not self.handle_fainted_creature(self.bot):
                    self._show_text(self.player, "You won!")
                    break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")
