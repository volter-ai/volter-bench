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

> Attack
> Swap"""

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
            self.resolve_turn(player_action, bot_action)

            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()

    def get_player_action(self, player: Player):
        if player.active_creature.hp <= 0:
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            if not available_creatures:
                self._show_text(player, f"{player.display_name} has no creatures left!")
                return None
                
            self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
            choice = self._wait_for_choice(player, [SelectThing(c) for c in available_creatures])
            player.active_creature = choice.thing
            return ("swap", choice.thing)

        while True:  # Main action menu loop
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(player, [attack_button, swap_button])

            if choice == attack_button:
                # Show skills with Back option
                back_button = Button("Back")
                choices = [SelectThing(s) for s in player.active_creature.skills]
                choices.append(back_button)
                
                skill_choice = self._wait_for_choice(player, choices)
                if skill_choice == back_button:
                    continue  # Go back to main action menu
                    
                return ("attack", skill_choice.thing)
            else:  # Swap selected
                available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
                if not available_creatures:
                    continue  # No valid swaps, return to main menu
                    
                # Show creatures with Back option
                back_button = Button("Back")
                choices = [SelectThing(c) for c in available_creatures]
                choices.append(back_button)
                
                creature_choice = self._wait_for_choice(player, choices)
                if creature_choice == back_button:
                    continue  # Go back to main action menu
                    
                return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"You switched to {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.bot.active_creature = bot_action[1]
            self._show_text(self.player, f"Foe switched to {bot_action[1].display_name}!")

        # Then handle attacks
        actions = []
        if player_action[0] == "attack":
            actions.append((self.player, self.bot, player_action[1]))
        if bot_action[0] == "attack":
            actions.append((self.bot, self.player, bot_action[1]))

        # Sort by speed
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        if len(actions) == 2 and actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
            random.shuffle(actions)

        # Execute attacks
        for attacker, defender, skill in actions:
            if attacker.active_creature.hp <= 0:
                continue
                
            damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            
            self._show_text(self.player, 
                f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
            self._show_text(self.player, f"It dealt {damage} damage!")

    def calculate_damage(self, attacker: Creature, defender: Creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def get_type_effectiveness(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

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
