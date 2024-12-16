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
        player_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP" 
            for c in self.player.creatures
        )
        bot_creatures_status = "\n".join(
            f"{c.display_name}: {c.hp}/{c.max_hp} HP" 
            for c in self.bot.creatures
        )
        
        return f"""=== Battle ===
Your Team:
{player_creatures_status}
Active: {self.player.active_creature.display_name}

Opponent's Team: 
{bot_creatures_status}
Active: {self.bot.active_creature.display_name}

> Attack
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            if not player_action:
                return
                
            # Bot turn
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                return

            # Resolve actions
            self.resolve_actions(player_action, bot_action)

            # Check for battle end
            if self.check_battle_end():
                return

    def get_player_action(self, player: Player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(player, [attack_button, swap_button])

            if choice == attack_button:
                # Show skills
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skill_choices + [back_button])
                
                if skill_choice == back_button:
                    continue
                    
                return {"type": "attack", "skill": skill_choice.thing}

            elif choice == swap_button:
                # Show available creatures
                available_creatures = [
                    c for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                creature_choices = [SelectThing(c) for c in available_creatures]
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, creature_choices + [back_button])
                
                if creature_choice == back_button:
                    continue
                    
                return {"type": "swap", "creature": creature_choice.thing}

    def resolve_actions(self, player_action, bot_action):
        # Handle swaps first
        if player_action["type"] == "swap":
            self.player.active_creature = player_action["creature"]
            self._show_text(self.player, f"You switched to {player_action['creature'].display_name}!")
            
        if bot_action["type"] == "swap":
            self.bot.active_creature = bot_action["creature"]
            self._show_text(self.player, f"Opponent switched to {bot_action['creature'].display_name}!")

        # Then handle attacks
        first_action, second_action = self.get_action_order(player_action, bot_action)
        self.execute_action(first_action[0], first_action[1])
        
        # Only execute second action if first didn't end battle
        if not self.check_battle_end():
            self.execute_action(second_action[0], second_action[1])

    def get_action_order(self, player_action, bot_action):
        if player_action["type"] == "attack" and bot_action["type"] == "attack":
            # Compare speeds
            if self.player.active_creature.speed > self.bot.active_creature.speed:
                return (self.player, player_action), (self.bot, bot_action)
            elif self.player.active_creature.speed < self.bot.active_creature.speed:
                return (self.bot, bot_action), (self.player, player_action)
            else:
                # Random if speeds are equal
                if random.random() < 0.5:
                    return (self.player, player_action), (self.bot, bot_action)
                return (self.bot, bot_action), (self.player, player_action)
        return (self.player, player_action), (self.bot, bot_action)

    def execute_action(self, attacker: Player, action: dict):
        if action["type"] == "attack":
            defender = self.bot if attacker == self.player else self.player
            self.execute_attack(attacker, defender, action["skill"])

    def execute_attack(self, attacker: Player, defender: Player, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = (
                attacker.active_creature.attack + 
                skill.base_damage - 
                defender.active_creature.defense
            )
        else:
            raw_damage = (
                (attacker.active_creature.sp_attack / 
                defender.active_creature.sp_defense) * 
                skill.base_damage
            )

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show message
        effectiveness = ""
        if multiplier > 1:
            effectiveness = "It's super effective!"
        elif multiplier < 1:
            effectiveness = "It's not very effective..."
            
        self._show_text(
            self.player,
            f"{attacker.active_creature.display_name} used {skill.display_name}! {effectiveness}"
        )

        # Handle fainting
        if defender.active_creature.hp <= 0:
            self._show_text(
                self.player,
                f"{defender.active_creature.display_name} was knocked out!"
            )
            self.handle_faint(defender)

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_faint(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        if player == self.player:
            self._show_text(self.player, "Choose your next creature!")
            creature_choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing
        else:
            # Bot chooses randomly
            player.active_creature = random.choice(available_creatures)
            self._show_text(
                self.player,
                f"Opponent sent out {player.active_creature.display_name}!"
            )

    def check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
            
        if not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene") 
            return True
            
        return False
