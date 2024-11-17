from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
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
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

Your Team:
{self._format_team(self.player)}

Foe's Team:
{self._format_team(self.bot)}"""

    def _format_team(self, player):
        return "\n".join([f"- {c.display_name}: {c.hp}/{c.max_hp} HP" for c in player.creatures])

    def run(self):
        while True:
            # Player turn
            player_action = self._get_player_action(self.player)
            bot_action = self._get_player_action(self.bot)
            
            # Execute actions
            self._resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self._check_battle_end():
                break

    def _get_valid_swap_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def _get_player_action(self, player):
        # Build available choices based on game state
        choices = [Button("Attack")]
        
        # Only offer swap if there are valid creatures to swap to
        valid_swap_creatures = self._get_valid_swap_creatures(player)
        if valid_swap_creatures:
            choices.append(Button("Swap"))
        
        choice = self._wait_for_choice(player, choices)
        
        if choice.display_name == "Attack":
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            return self._wait_for_choice(player, skill_choices)
        else:
            creature_choices = [SelectThing(creature) for creature in valid_swap_creatures]
            return self._wait_for_choice(player, creature_choices)

    def _resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action.thing, Creature):
            self.player.active_creature = player_action.thing
            self._show_text(self.player, f"You switched to {player_action.thing.display_name}!")
            
        if isinstance(bot_action.thing, Creature):
            self.bot.active_creature = bot_action.thing
            self._show_text(self.player, f"Foe switched to {bot_action.thing.display_name}!")

        # Then handle attacks
        first, second = self._determine_order(player_action, bot_action)
        self._execute_action(first)
        if self._check_battle_end():
            return
        self._execute_action(second)

    def _determine_order(self, player_action, bot_action):
        if isinstance(player_action.thing, Creature) or isinstance(bot_action.thing, Creature):
            return player_action, bot_action
            
        if self.player.active_creature.speed > self.bot.active_creature.speed:
            return player_action, bot_action
        elif self.player.active_creature.speed < self.bot.active_creature.speed:
            return bot_action, player_action
        else:
            return random.choice([(player_action, bot_action), (bot_action, player_action)])

    def _execute_action(self, action):
        if isinstance(action.thing, Creature):
            return
            
        attacker = self.player if action.thing in self.player.active_creature.skills else self.bot
        defender = self.bot if attacker == self.player else self.player
        
        skill = action.thing
        damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        
        self._show_text(self.player, 
            f"{'You' if attacker == self.player else 'Foe'} used {skill.display_name}! "
            f"It dealt {damage} damage!")
        
        if defender.active_creature.hp == 0:
            self._handle_knockout(defender)

    def _calculate_damage(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def _get_type_multiplier(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)

    def _handle_knockout(self, player):
        self._show_text(self.player, 
            f"{'Your' if player == self.player else 'Foe'} {player.active_creature.display_name} was knocked out!")
            
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        if not valid_creatures:
            return
            
        creature_choices = [SelectThing(creature) for creature in valid_creatures]
        new_creature = self._wait_for_choice(player, creature_choices).thing
        player.active_creature = new_creature
        
        self._show_text(self.player,
            f"{'You' if player == self.player else 'Foe'} sent out {new_creature.display_name}!")

    def _check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            self._show_text(self.player, "You won!" if bot_alive else "You lost!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
