from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
from main_game.models import Creature, Skill
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

> Attack
> Swap (if you have other creatures available)"""

    def run(self):
        while True:
            # Player Choice Phase
            player_action = self.get_player_action(self.player)
            if not player_action:
                continue  # Player chose "Back", restart turn
                
            # Foe Choice Phase
            bot_action = self.get_player_action(self.bot)
            
            # Resolution Phase
            action_queue = []
            
            # Add swaps to queue first
            if isinstance(player_action.thing, Creature):
                action_queue.append(("swap", self.player, player_action.thing))
            if isinstance(bot_action.thing, Creature):
                action_queue.append(("swap", self.bot, bot_action.thing))
                
            # Add attacks to queue with speed-based ordering
            if isinstance(player_action.thing, Skill) and isinstance(bot_action.thing, Skill):
                if self.player.active_creature.speed > self.bot.active_creature.speed:
                    action_queue.extend([
                        ("attack", self.player, player_action.thing),
                        ("attack", self.bot, bot_action.thing)
                    ])
                elif self.player.active_creature.speed < self.bot.active_creature.speed:
                    action_queue.extend([
                        ("attack", self.bot, bot_action.thing),
                        ("attack", self.player, player_action.thing)
                    ])
                else:
                    # Random order on speed tie
                    attackers = [(self.player, player_action.thing), (self.bot, bot_action.thing)]
                    random.shuffle(attackers)
                    action_queue.extend([
                        ("attack", attacker, action) for attacker, action in attackers
                    ])
            
            # Execute action queue
            self.resolve_action_queue(action_queue)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player):
        while True:
            # Main choice menu
            choices = [Button("Attack")]
            if self.get_available_creatures(player):
                choices.append(Button("Swap"))
            
            main_choice = self._wait_for_choice(player, choices)
            
            if main_choice.display_name == "Attack":
                # Attack submenu
                back_button = Button("Back")
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                skill_choices.append(back_button)
                
                choice = self._wait_for_choice(player, skill_choices)
                if isinstance(choice, Button):
                    continue
                return choice
            else:
                # Swap submenu
                back_button = Button("Back")
                available_creatures = self.get_available_creatures(player)
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                creature_choices.append(back_button)
                
                choice = self._wait_for_choice(player, creature_choices)
                if isinstance(choice, Button):
                    continue
                return choice

    def get_available_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def resolve_action_queue(self, action_queue):
        for action_type, actor, thing in action_queue:
            if action_type == "swap":
                actor.active_creature = thing
                self._show_text(actor, f"{actor.display_name} swapped to {thing.display_name}!")
            elif action_type == "attack":
                defender = self.bot if actor == self.player else self.player
                self.execute_skill(actor, defender, thing)

    def execute_skill(self, attacker, defender, skill):
        if defender.active_creature.hp <= 0:
            return
            
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
        
        if defender.active_creature.hp <= 0:
            self.handle_knockout(defender)

    def get_type_multiplier(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def handle_knockout(self, player):
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        
        available_creatures = self.get_available_creatures(player)
        if not available_creatures:
            return
            
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        new_creature = self._wait_for_choice(player, creature_choices).thing
        player.active_creature = new_creature

    def check_battle_end(self):
        player_alive = any(c.hp > 0 for c in self.player.creatures)
        bot_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_alive or not bot_alive:
            winner = self.player if player_alive else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        return False
