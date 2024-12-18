from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Reset creatures
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
> Swap"""

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player.active_creature.display_name} vs {self.bot.active_creature.display_name}")
        
        while True:
            # Player Choice Phase
            player_action = self.choice_phase(self.player)
            
            # Foe Choice Phase
            bot_action = self.choice_phase(self.bot)
            
            # Resolution Phase
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def choice_phase(self, current_player):
        while True:
            # Main menu choices
            choices = [Button("Attack")]
            if self.get_available_creatures(current_player):
                choices.append(Button("Swap"))
            
            main_choice = self._wait_for_choice(current_player, choices)
            
            if main_choice.display_name == "Attack":
                # Attack submenu
                choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
                choices.append(Button("Back"))
                
                skill_choice = self._wait_for_choice(current_player, choices)
                if skill_choice.display_name == "Back":
                    continue
                return skill_choice
                
            else:  # Swap
                # Swap submenu
                available_creatures = self.get_available_creatures(current_player)
                choices = [SelectThing(creature) for creature in available_creatures]
                choices.append(Button("Back"))
                
                creature_choice = self._wait_for_choice(current_player, choices)
                if creature_choice.display_name == "Back":
                    continue
                return creature_choice

    def get_available_creatures(self, current_player):
        return [c for c in current_player.creatures if c.hp > 0 and c != current_player.active_creature]

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
            self._show_text(self.player, f"You swapped to {player_action.thing.display_name}!")
            
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            self._show_text(self.player, f"Foe swapped to {bot_action.thing.display_name}!")

        # Then handle attacks
        first, second = self.determine_order(player_action, bot_action)
        self.execute_action(first, player_action, bot_action)
        if self.check_battle_end():
            return
        self.execute_action(second, player_action, bot_action)

    def determine_order(self, player_action, bot_action):
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_action, bot_action
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return bot_action, player_action
        else:
            import random
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def execute_action(self, action, player_action, bot_action):
        if isinstance(action.thing, Creature):
            return  # Swaps already handled
            
        skill = action.thing
        attacker = self.player if action == player_action else self.bot
        defender = self.bot if action == player_action else self.player
        
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        self._show_text(self.player, f"{attacker.active_creature.display_name} used {skill.display_name}! Dealt {final_damage} damage!")
        
        if defender.active_creature.hp == 0:
            self.handle_knockout(defender)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, player):
        self._show_text(self.player, f"{player.active_creature.display_name} was knocked out!")
        
        available_creatures = self.get_available_creatures(player)
        if not available_creatures:
            return
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        new_creature = self._wait_for_choice(player, creature_choices).thing
        player.active_creature = new_creature
        self._show_text(self.player, f"{'You' if player == self.player else 'Foe'} sent out {new_creature.display_name}!")

    def check_battle_end(self):
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
