from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.bot.display_name}'s {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                continue
                
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            self.check_battle_end()

    def get_player_action(self, player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")
        
        while True:
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Show skills
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(back_button)
                
                skill_choice = self._wait_for_choice(player, skill_choices)
                if skill_choice == back_button:
                    continue
                    
                return ("attack", skill_choice.thing)
                
            elif choice == swap_button:
                # Show available creatures
                available_creatures = [c for c in player.creatures 
                                    if c != player.active_creature and c.hp > 0]
                if not available_creatures:
                    self._show_text(player, "No creatures available to swap!")
                    continue
                    
                creature_choices = [SelectThing(c) for c in available_creatures]
                creature_choices.append(back_button)
                
                creature_choice = self._wait_for_choice(player, creature_choices)
                if creature_choice == back_button:
                    continue
                    
                return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"Go {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.bot, f"Go {bot_action[1].display_name}!")
            
        # Then handle attacks
        if player_action[0] == "attack" and bot_action[0] == "attack":
            # Determine order based on speed
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                first, second = (self.player, player_action[1]), (self.bot, bot_action[1])
            elif self.player.active_creature.speed < self.bot.active_creature.speed:
                first, second = (self.bot, bot_action[1]), (self.player, player_action[1])
            else:
                if random.random() < 0.5:
                    first, second = (self.player, player_action[1]), (self.bot, bot_action[1])
                else:
                    first, second = (self.bot, bot_action[1]), (self.player, player_action[1])
                    
            self.execute_attack(first[0], first[1])
            if not self.check_battle_end():
                self.execute_attack(second[0], second[1])

    def execute_attack(self, attacker, skill):
        if attacker == self.player:
            defender = self.bot
        else:
            defender = self.player
            
        # Calculate damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         defender.active_creature.defense)
        else:
            raw_damage = (skill.base_damage * 
                         attacker.active_creature.sp_attack / 
                         defender.active_creature.sp_defense)
            
        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, 
                                                 defender.active_creature.creature_type)
        
        final_damage = int(raw_damage * effectiveness)
        defender.active_creature.hp -= final_damage
        
        self._show_text(attacker, 
                       f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, 
                       f"{defender.active_creature.display_name} took {final_damage} damage!")

    def get_type_effectiveness(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(attack_type, {}).get(defend_type, 1.0)

    def check_battle_end(self):
        def check_player_loss(player):
            return all(c.hp <= 0 for c in player.creatures)
            
        if check_player_loss(self.player):
            self._show_text(self.player, "You lost the battle!")
            self._quit_whole_game()  # Properly end the game
            return True
            
        if check_player_loss(self.bot):
            self._show_text(self.player, "You won the battle!")
            self._quit_whole_game()  # Properly end the game
            return True
            
        if (self.player.active_creature.hp <= 0 or 
            self.bot.active_creature.hp <= 0):
            self.handle_knockouts()
            
        return False

    def handle_knockouts(self):
        for player in [self.player, self.bot]:
            if player.active_creature.hp <= 0:
                self._show_text(player, 
                              f"{player.active_creature.display_name} was knocked out!")
                              
                available_creatures = [c for c in player.creatures if c.hp > 0]
                if available_creatures:
                    creature_choices = [SelectThing(c) for c in available_creatures]
                    choice = self._wait_for_choice(player, creature_choices)
                    player.active_creature = choice.thing
                    self._show_text(player, f"Go {choice.thing.display_name}!")
