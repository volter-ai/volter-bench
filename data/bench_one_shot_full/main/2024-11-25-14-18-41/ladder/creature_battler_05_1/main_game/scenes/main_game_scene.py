from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, create_from_game_database
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creatures by recreating them from prototypes
        self.player.creatures = [
            create_from_game_database(c.prototype_id, c.__class__) 
            for c in self.player.creatures
        ]
        self.bot.creatures = [
            create_from_game_database(c.prototype_id, c.__class__)
            for c in self.bot.creatures
        ]
        
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Foe's {bot_creature.display_name}: {bot_creature.hp}/{bot_creature.max_hp} HP

What will you do?
> Attack
> Swap"""

    def run(self):
        while True:
            # Keep getting actions until both players have valid actions
            while True:
                player_action = self.get_player_action(self.player)
                if not player_action:
                    continue
                    
                bot_action = self.get_bot_action(self.bot)
                # Bot actions should never be None now
                break
                
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Reset creatures by recreating them before leaving
                self.player.creatures = [
                    create_from_game_database(c.prototype_id, c.__class__)
                    for c in self.player.creatures
                ]
                self.player.active_creature = None
                # Return to main menu after battle ends
                self._transition_to_scene("MainMenuScene")
                return

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            return self.choose_attack(player, include_back=True)
        else:
            return self.choose_swap(player, include_back=True)

    def get_bot_action(self, bot):
        # Bot randomly chooses between attack and swap
        if random.random() < 0.8:  # 80% chance to attack
            return self.choose_attack(bot, include_back=False)
        return self.choose_swap(bot, include_back=False)

    def choose_attack(self, player, include_back=True):
        choices = [SelectThing(skill) for skill in player.active_creature.skills]
        if include_back:
            back_button = Button("Back")
            choices.append(back_button)
            
            choice = self._wait_for_choice(player, choices)
            if choice == back_button:
                return None
        else:
            choice = self._wait_for_choice(player, choices)
            
        return ("attack", choice.thing)

    def choose_swap(self, player, include_back=True):
        available_creatures = [c for c in player.creatures 
                             if c != player.active_creature and c.hp > 0]
        if not available_creatures:
            self._show_text(player, "No other creatures available!")
            return None
            
        choices = [SelectThing(creature) for creature in available_creatures]
        if include_back:
            back_button = Button("Back")
            choices.append(back_button)
            
            choice = self._wait_for_choice(player, choices)
            if choice == back_button:
                return None
        else:
            choice = self._wait_for_choice(player, choices)
            
        return ("swap", choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"Go {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Foe sent out {bot_action[1].display_name}!")

        # Then resolve attacks
        if player_action[0] == "attack" and bot_action[0] == "attack":
            # Determine order based on speed
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                self.execute_attack(self.player, self.bot, player_action[1])
                if self.bot.active_creature.hp > 0:
                    self.execute_attack(self.bot, self.player, bot_action[1])
            else:
                self.execute_attack(self.bot, self.player, bot_action[1])
                if self.player.active_creature.hp > 0:
                    self.execute_attack(self.player, self.bot, player_action[1])

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         defender.active_creature.defense)
        else:
            raw_damage = (attacker.active_creature.sp_attack / 
                         defender.active_creature.sp_defense * 
                         skill.base_damage)
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, 
                                            defender.active_creature.creature_type)
        
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
                       f"{attacker.active_creature.display_name} used {skill.display_name}!")
        
        if multiplier > 1:
            self._show_text(self.player, "It's super effective!")
        elif multiplier < 1:
            self._show_text(self.player, "It's not very effective...")

    def get_type_multiplier(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def check_battle_end(self):
        def has_available_creatures(player):
            return any(c.hp > 0 for c in player.creatures)
            
        if self.player.active_creature.hp <= 0:
            if not has_available_creatures(self.player):
                self._show_text(self.player, "You lost the battle!")
                return True
            self.force_swap(self.player)
            
        if self.bot.active_creature.hp <= 0:
            if not has_available_creatures(self.bot):
                self._show_text(self.player, "You won the battle!")
                return True
            self.force_swap(self.bot)
            
        return False

    def force_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures]
        
        self._show_text(self.player, 
                       f"{player.active_creature.display_name} was knocked out!")
        
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        self._show_text(self.player, 
                       f"Go {player.active_creature.display_name}!")
