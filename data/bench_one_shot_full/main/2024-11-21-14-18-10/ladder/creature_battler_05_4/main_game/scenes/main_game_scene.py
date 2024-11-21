from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.initialize_creatures()

    def initialize_creatures(self):
        # Reset creatures and set initial active creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Enemy {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Return to main menu after battle ends
                self._transition_to_scene("MainMenuScene")
                return

    def get_player_action(self, current_player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(current_player, [attack_button, swap_button])

            if choice == attack_button:
                # Show skills
                skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(current_player, skill_choices + [back_button])
                
                if skill_choice != back_button:
                    return ("attack", skill_choice.thing)
                
            elif choice == swap_button:
                # Show available creatures
                available_creatures = [c for c in current_player.creatures 
                                    if c != current_player.active_creature and c.hp > 0]
                if not available_creatures:
                    self._show_text(current_player, "No other creatures available!")
                    continue
                    
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(current_player, creature_choices + [back_button])
                
                if creature_choice != back_button:
                    return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"You switched to {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Opponent switched to {bot_action[1].display_name}!")

        # Then handle attacks
        first_action, second_action = self.determine_order(player_action, bot_action)
        first_player = self.player if first_action == player_action else self.bot
        second_player = self.player if second_action == player_action else self.bot
        
        self.execute_action(first_action, first_player)
        if self.check_battle_end():
            return
        self.execute_action(second_action, second_player)

    def determine_order(self, player_action, bot_action):
        if player_action[0] == "swap" or bot_action[0] == "swap":
            return player_action, bot_action
            
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_action, bot_action
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return bot_action, player_action
        else:
            import random
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def execute_action(self, action, attacker):
        if action[0] == "attack":
            defender = self.bot if attacker == self.player else self.player
            skill = action[1]
            damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
            
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            self._show_text(self.player, 
                f"{'You' if attacker == self.player else 'Opponent'} used {skill.display_name}! "
                f"Dealt {damage} damage!")

            if defender.active_creature.hp == 0:
                self.handle_fainted_creature(defender)

    def calculate_damage(self, attacker: Creature, defender: Creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def handle_fainted_creature(self, player: Player):
        self._show_text(self.player, 
            f"{'Your' if player == self.player else 'Opponent''s'} "
            f"{player.active_creature.display_name} fainted!")
            
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            if len(available_creatures) == 1:
                player.active_creature = available_creatures[0]
                self._show_text(self.player,
                    f"{'You' if player == self.player else 'Opponent'} sent out {player.active_creature.display_name}!")
            else:
                creature_choices = [SelectThing(c) for c in available_creatures]
                choice = self._wait_for_choice(player, creature_choices)
                player.active_creature = choice.thing
                self._show_text(self.player,
                    f"{'You' if player == self.player else 'Opponent'} sent out {player.active_creature.display_name}!")

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
