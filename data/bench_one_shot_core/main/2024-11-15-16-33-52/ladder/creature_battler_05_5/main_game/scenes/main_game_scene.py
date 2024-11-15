from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
from typing import List, Tuple
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self._initialize_battle()

    def _initialize_battle(self):
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
> Swap
"""

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Calculate type multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": multiplier = 2.0
            elif defender.creature_type == "water": multiplier = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": multiplier = 2.0
            elif defender.creature_type == "leaf": multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": multiplier = 2.0
            elif defender.creature_type == "fire": multiplier = 0.5

        return int(raw_damage * multiplier)

    def _get_available_creatures(self, player: Player) -> List[Creature]:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def _get_player_action(self) -> dict:
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(self.player, [attack_button, swap_button])

            if choice == attack_button:
                skill_choices = [SelectThing(skill) for skill in self.player.active_creature.skills]
                back_button = Button("Back")
                skill_choices.append(back_button)
                
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                if skill_choice == back_button:
                    continue
                    
                return {"type": "attack", "skill": skill_choice.thing}
            else:
                available = self._get_available_creatures(self.player)
                if available:
                    creature_choices = [SelectThing(creature) for creature in available]
                    back_button = Button("Back")
                    creature_choices.append(back_button)
                    
                    creature_choice = self._wait_for_choice(self.player, creature_choices)
                    if creature_choice == back_button:
                        continue
                        
                    return {"type": "swap", "creature": creature_choice.thing}
                return {}  # No available creatures to swap to

    def _handle_turn(self) -> Tuple[dict, dict]:
        # Get player action
        player_action = self._get_player_action()

        # Get bot action
        bot_action = {}
        if random.random() < 0.8:  # 80% chance to attack
            bot_action = {
                "type": "attack",
                "skill": random.choice(self.bot.active_creature.skills)
            }
        else:
            available = self._get_available_creatures(self.bot)
            if available:
                bot_action = {
                    "type": "swap",
                    "creature": random.choice(available)
                }

        return player_action, bot_action

    def _resolve_turn(self, player_action: dict, bot_action: dict):
        # Handle swaps first
        if player_action.get("type") == "swap":
            self.player.active_creature = player_action["creature"]
        if bot_action.get("type") == "swap":
            self.bot.active_creature = bot_action["creature"]

        # Handle attacks based on speed
        if player_action.get("type") == "attack" and bot_action.get("type") == "attack":
            # Determine order based on speed, with random resolution for ties
            if self.player.active_creature.speed == self.bot.active_creature.speed:
                first = random.choice([self.player, self.bot])
            else:
                first = self.player if self.player.active_creature.speed > self.bot.active_creature.speed else self.bot
            
            second = self.bot if first == self.player else self.player
            first_action = player_action if first == self.player else bot_action
            second_action = bot_action if first == self.player else player_action

            # First attack
            damage = self._calculate_damage(first.active_creature, second.active_creature, first_action["skill"])
            second.active_creature.hp = max(0, second.active_creature.hp - damage)
            self._show_text(self.player, f"{first.active_creature.display_name} used {first_action['skill'].display_name}!")

            # Second attack if creature still alive
            if second.active_creature.hp > 0:
                damage = self._calculate_damage(second.active_creature, first.active_creature, second_action["skill"])
                first.active_creature.hp = max(0, first.active_creature.hp - damage)
                self._show_text(self.player, f"{second.active_creature.display_name} used {second_action['skill'].display_name}!")

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Check for fainted creatures
            if self.player.active_creature.hp == 0:
                available = self._get_available_creatures(self.player)
                if not available:
                    self._show_text(self.player, "You lost!")
                    break
                creature_choices = [SelectThing(creature) for creature in available]
                new_creature = self._wait_for_choice(self.player, creature_choices).thing
                self.player.active_creature = new_creature

            if self.bot.active_creature.hp == 0:
                available = self._get_available_creatures(self.bot)
                if not available:
                    self._show_text(self.player, "You won!")
                    break
                self.bot.active_creature = random.choice(available)

            # Handle turn
            player_action, bot_action = self._handle_turn()
            self._resolve_turn(player_action, bot_action)

        self._transition_to_scene("MainMenuScene")
