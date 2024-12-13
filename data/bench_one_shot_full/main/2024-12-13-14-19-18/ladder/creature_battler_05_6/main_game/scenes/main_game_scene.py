from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.reset_creatures()

    def reset_creatures(self):
        # Reset all creatures to full HP
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
{"> Swap" if self.get_available_creatures(self.player) else ""}
"""

    def get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal" or creature_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        return int(raw_damage * multiplier)

    def execute_turn(self, player_action, bot_action):
        # Handle swaps first
        if isinstance(player_action, SelectThing):
            self.player.active_creature = player_action.thing
        if isinstance(bot_action, SelectThing):
            self.bot.active_creature = bot_action.thing

        # Then handle attacks
        actions = [(self.player, player_action), (self.bot, bot_action)]
        if isinstance(player_action, Button) and isinstance(bot_action, Button):
            # Sort by speed for attack order
            actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
            if actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
                random.shuffle(actions)

        for attacker, action in actions:
            if isinstance(action, Button):
                defender = self.bot if attacker == self.player else self.player
                skill = action.skill
                damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
                defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
                self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
                self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")

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

    def run(self):
        while True:
            # Build choice list based on available options
            choices = [Button("Attack")]
            available_creatures = self.get_available_creatures(self.player)
            if available_creatures:
                choices.append(Button("Swap"))
            
            choice = self._wait_for_choice(self.player, choices)

            player_action = None
            if choice == choices[0]:  # Attack
                skill_choices = [Button(skill.display_name) for skill in self.player.active_creature.skills]
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                skill_choice.skill = self.player.active_creature.skills[skill_choices.index(skill_choice)]
                player_action = skill_choice
            else:  # Swap
                swap_choices = [SelectThing(c) for c in available_creatures]
                player_action = self._wait_for_choice(self.player, swap_choices)

            # Bot turn
            bot_action = self._wait_for_choice(self.bot, [Button("Attack")])
            if bot_action:
                skill = random.choice(self.bot.active_creature.skills)
                bot_action.skill = skill

            # Execute turn
            self.execute_turn(player_action, bot_action)

            # Check for fainted creatures
            if self.player.active_creature.hp <= 0:
                if not self.handle_fainted_creature(self.player):
                    self._show_text(self.player, "You lost!")
                    break
            if self.bot.active_creature.hp <= 0:
                if not self.handle_fainted_creature(self.bot):
                    self._show_text(self.player, "You won!")
                    break

        self._transition_to_scene("MainMenuScene")
