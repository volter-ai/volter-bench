from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, RandomModeGracefulExit
from main_game.models import Player, Creature

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
{"> Swap" if self.has_valid_swap_targets(self.player) else ""}
"""

    def run(self):
        try:
            while True:
                # Player turn
                player_action = self.get_player_action(self.player)
                bot_action = self.get_player_action(self.bot)
                
                # Resolve actions
                self.resolve_turn(player_action, bot_action)
                
                # Check for battle end
                if self.check_battle_end():
                    break
        except RandomModeGracefulExit:
            pass
        finally:
            self._transition_to_scene("MainMenuScene")

    def has_valid_swap_targets(self, player):
        return any(c.hp > 0 and c != player.active_creature for c in player.creatures)

    def get_player_action(self, player):
        while True:
            # Main choice menu
            choices = [Button("Attack")]
            if self.has_valid_swap_targets(player):
                choices.append(Button("Swap"))
        
            choice = self._wait_for_choice(player, choices)
            
            if choice.display_name == "Attack":
                # Attack submenu
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(Button("Back"))
                
                skill_choice = self._wait_for_choice(player, skill_choices)
                
                if skill_choice.display_name == "Back":
                    continue  # Go back to main menu
                    
                return {"type": "attack", "skill": skill_choice.thing}
                
            else:  # Swap
                # Swap submenu
                valid_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                swap_choices = [SelectThing(creature) for creature in valid_creatures]
                swap_choices.append(Button("Back"))
                
                swap_choice = self._wait_for_choice(player, swap_choices)
                
                if swap_choice.display_name == "Back":
                    continue  # Go back to main menu
                    
                return {"type": "swap", "creature": swap_choice.thing}

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]

        # Then handle attacks based on speed
        if player_action["type"] == "attack" and bot_action["type"] == "attack":
            if self.player.active_creature.speed >= self.bot.active_creature.speed:
                self.execute_attack(self.player, self.bot, player_action["skill"])
                if self.bot.active_creature.hp > 0:
                    self.execute_attack(self.bot, self.player, bot_action["skill"])
            else:
                self.execute_attack(self.bot, self.player, bot_action["skill"])
                if self.player.active_creature.hp > 0:
                    self.execute_attack(self.player, self.bot, player_action["skill"])

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
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
            self._show_text(defender, f"{defender.active_creature.display_name} fainted!")
            
            # Check if battle should end
            if not any(c.hp > 0 for c in defender.creatures):
                return
                
            # Handle forced swap
            valid_creatures = [c for c in defender.creatures if c.hp > 0]
            choices = [SelectThing(creature) for creature in valid_creatures]
            defender.active_creature = self._wait_for_choice(defender, choices).thing

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

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
