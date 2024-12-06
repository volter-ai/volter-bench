from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.reset_creatures()

    def reset_creatures(self):
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

> Attack
> Swap"""

    def calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Type effectiveness - explicitly handle normal type
        effectiveness = 1.0
        if skill.skill_type == "normal":
            effectiveness = 1.0  # Normal is neutral against everything
        elif skill.skill_type == "fire":
            if defender.creature_type == "leaf": effectiveness = 2.0
            elif defender.creature_type == "water": effectiveness = 0.5
        elif skill.skill_type == "water":
            if defender.creature_type == "fire": effectiveness = 2.0
            elif defender.creature_type == "leaf": effectiveness = 0.5
        elif skill.skill_type == "leaf":
            if defender.creature_type == "water": effectiveness = 2.0
            elif defender.creature_type == "fire": effectiveness = 0.5

        return int(raw_damage * effectiveness)

    def execute_turn(self, p1: Player, p2: Player, p1_action, p2_action):
        # Handle swaps first
        if isinstance(p1_action, Creature):
            p1.active_creature = p1_action
        if isinstance(p2_action, Creature):
            p2.active_creature = p2_action

        # Only proceed with damage if both actions are Skills
        if isinstance(p1_action, Skill) and isinstance(p2_action, Skill):
            first = p1 if p1.active_creature.speed > p2.active_creature.speed or \
                        (p1.active_creature.speed == p2.active_creature.speed and random.random() < 0.5) else p2
            second = p2 if first == p1 else p1
            first_action = p1_action if first == p1 else p2_action
            second_action = p2_action if first == p1 else p1_action

            damage = self.calculate_damage(first.active_creature, second.active_creature, first_action)
            second.active_creature.hp -= damage
            if second.active_creature.hp > 0:
                damage = self.calculate_damage(second.active_creature, first.active_creature, second_action)
                first.active_creature.hp -= damage

    def get_available_creatures(self, player: Player) -> list[Creature]:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def handle_fainted(self, player: Player) -> bool:
        if player.active_creature.hp <= 0:
            available = self.get_available_creatures(player)
            if not available:
                return False
            
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            
        return True

    def get_player_choice(self, player: Player):
        while True:
            # Main choice
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(player, [attack_button, swap_button])

            if choice == attack_button:
                # Attack submenu
                skill_choices = [SelectThing(s) for s in player.active_creature.skills]
                back_button = Button("Back")
                choice = self._wait_for_choice(player, skill_choices + [back_button])
                
                if choice == back_button:
                    continue
                return choice.thing
            else:
                # Swap submenu
                creature_choices = [SelectThing(c) for c in self.get_available_creatures(player)]
                if not creature_choices:
                    continue
                    
                back_button = Button("Back")
                choice = self._wait_for_choice(player, creature_choices + [back_button])
                
                if choice == back_button:
                    continue
                return choice.thing

    def run(self):
        while True:
            # Player Choice Phase
            player_action = self.get_player_choice(self.player)

            # Foe Choice Phase - bot follows same choice structure
            bot_action = self.get_player_choice(self.bot)

            # Execute turn
            self.execute_turn(self.player, self.bot, player_action, bot_action)

            # Check for fainted creatures
            if not self.handle_fainted(self.player):
                self._show_text(self.player, "You lost!")
                break
            if not self.handle_fainted(self.bot):
                self._show_text(self.player, "You won!")
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")
