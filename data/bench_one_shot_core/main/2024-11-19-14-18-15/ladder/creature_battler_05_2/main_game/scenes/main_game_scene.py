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
{"> Swap" if any(c.hp > 0 and c != self.player.active_creature for c in self.player.creatures) else ""}
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()

    def get_player_action(self, player: Player):
        choices = [Button("Attack")]
        
        # Only add swap option if there are valid creatures to swap to
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
        if available_creatures:
            choices.append(Button("Swap"))
        
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            # Show skills with Back option
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            skill_choices.append(Button("Back"))
            
            choice = self._wait_for_choice(player, skill_choices)
            
            # If Back was chosen, recursively get new action
            if isinstance(choice, Button) and choice.display_name == "Back":
                return self.get_player_action(player)
            return choice
        else:
            # Show available creatures with Back option
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            creature_choices.append(Button("Back"))
            
            choice = self._wait_for_choice(player, creature_choices)
            
            # If Back was chosen, recursively get new action
            if isinstance(choice, Button) and choice.display_name == "Back":
                return self.get_player_action(player)
            return choice

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
            self._show_text(self.player, f"You sent out {player_action.thing.display_name}!")
            
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            self._show_text(self.player, f"Foe sent out {bot_action.thing.display_name}!")

        # Handle attacks
        actions = []
        if isinstance(player_action.thing, Skill):
            actions.append((self.player, player_action.thing))
        if isinstance(bot_action.thing, Skill):
            actions.append((self.bot, bot_action.thing))
            
        # Sort by speed, with random tiebreaker for equal speeds
        if len(actions) == 2:
            player_speed = actions[0][0].active_creature.speed
            bot_speed = actions[1][0].active_creature.speed
            
            if player_speed == bot_speed:
                # Random order for equal speeds
                actions = random.sample(actions, len(actions))
            else:
                # Sort by speed normally
                actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        # Execute attacks
        for attacker, skill in actions:
            defender = self.bot if attacker == self.player else self.player
            self.execute_skill(attacker, defender, skill)

    def execute_skill(self, attacker: Player, defender: Player, skill: Skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Calculate type multiplier
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        
        # Apply damage
        final_damage = int(raw_damage * multiplier)
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}!")
        
        # Force swap if creature fainted
        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} fainted!")
            self.force_swap(defender)

    def get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def force_swap(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        if len(available_creatures) == 1:
            player.active_creature = available_creatures[0]
            self._show_text(self.player, f"{'You' if player == self.player else 'Foe'} sent out {player.active_creature.display_name}!")
        else:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing
            self._show_text(self.player, f"{'You' if player == self.player else 'Foe'} sent out {player.active_creature.display_name}!")

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
