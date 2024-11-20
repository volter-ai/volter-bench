from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature
import random

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

    def _get_available_creatures(self, player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def _execute_skill(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = 1.0
        if skill.skill_type == "fire":
            if defender.creature_type == "leaf": effectiveness = 2.0
            elif defender.creature_type == "water": effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": effectiveness = 2.0
            elif defender.creature_type == "leaf": effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": effectiveness = 2.0
            elif defender.creature_type == "fire": effectiveness = 0.5

        final_damage = int(raw_damage * effectiveness)
        defender.hp = max(0, defender.hp - final_damage)

        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        if effectiveness > 1:
            self._show_text(self.player, "It's super effective!")
        elif effectiveness < 1:
            self._show_text(self.player, "It's not very effective...")

    def _handle_player_turn(self, player):
        while True:
            choice = self._wait_for_choice(player, [
                Button("Attack"),
                Button("Swap"),
            ])

            if choice.display_name == "Attack":
                skills = [SelectThing(skill) for skill in player.active_creature.skills]
                skills.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skills)
                
                if isinstance(skill_choice, Button):
                    continue
                    
                return ("attack", skill_choice.thing)

            elif choice.display_name == "Swap":
                available = [SelectThing(c) for c in self._get_available_creatures(player)]
                available.append(Button("Back"))
                swap_choice = self._wait_for_choice(player, available)
                
                if isinstance(swap_choice, Button):
                    continue
                    
                return ("swap", swap_choice.thing)

    def run(self):
        while True:
            # Player turn
            player_action = self._handle_player_turn(self.player)
            
            # Bot turn
            bot_action = self._handle_player_turn(self.bot)
            
            # Resolution phase
            if player_action[0] == "swap":
                self.player.active_creature = player_action[1]
                self._show_text(self.player, f"You switched to {player_action[1].display_name}!")
                
            if bot_action[0] == "swap":
                self.bot.active_creature = bot_action[1]
                self._show_text(self.player, f"Foe switched to {bot_action[1].display_name}!")

            # Execute attacks based on speed
            if player_action[0] == "attack" and bot_action[0] == "attack":
                player_speed = self.player.active_creature.speed
                bot_speed = self.bot.active_creature.speed
                
                # Determine order based on speed with random tiebreaker
                if player_speed > bot_speed:
                    first, second = self.player, self.bot
                    first_skill = player_action[1]
                    second_skill = bot_action[1]
                elif player_speed < bot_speed:
                    first, second = self.bot, self.player
                    first_skill = bot_action[1]
                    second_skill = player_action[1]
                else:
                    # Equal speed - random order
                    if random.choice([True, False]):
                        first, second = self.player, self.bot
                        first_skill = player_action[1]
                        second_skill = bot_action[1]
                    else:
                        first, second = self.bot, self.player
                        first_skill = bot_action[1]
                        second_skill = player_action[1]

                self._execute_skill(first.active_creature, second.active_creature, first_skill)
                if second.active_creature.hp > 0:
                    self._execute_skill(second.active_creature, first.active_creature, second_skill)

            # Check for knockouts and handle swaps
            for current_player in [self.player, self.bot]:
                if current_player.active_creature.hp <= 0:
                    available = self._get_available_creatures(current_player)
                    if not available:
                        winner = self.player if current_player == self.bot else self.bot
                        self._show_text(self.player, f"{winner.display_name} wins!")
                        self._quit_whole_game()
                        
                    self._show_text(self.player, f"{current_player.active_creature.display_name} was knocked out!")
                    swap_choices = [SelectThing(c) for c in available]
                    swap = self._wait_for_choice(current_player, swap_choices)
                    current_player.active_creature = swap.thing
                    self._show_text(self.player, f"{current_player.display_name} sent out {swap.thing.display_name}!")
