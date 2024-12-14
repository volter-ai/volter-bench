from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Player
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
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap
"""

    def _execute_skill(self, attacker: Creature, defender: Creature, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"Dealt {final_damage} damage!")

    def _get_type_effectiveness(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
        
        effectiveness_map = {
            ("fire", "leaf"): 2.0,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2.0,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2.0,
            ("leaf", "fire"): 0.5
        }
        
        return effectiveness_map.get((skill_type, defender_type), 1.0)

    def _handle_knocked_out(self, player: Player) -> bool:
        # Returns True if player can continue, False if they lost
        if player.active_creature.hp > 0:
            return True
            
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return False
            
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        choices = [SelectThing(c) for c in available_creatures]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return True

    def run(self):
        while True:
            # Player turn
            player_action = self._get_player_action(self.player)
            bot_action = self._get_player_action(self.bot)

            # Resolve actions
            first_player, second_player = self._determine_turn_order(
                self.player, player_action,
                self.bot, bot_action
            )

            # Execute actions
            for current_player, action in [first_player, second_player]:
                if isinstance(action, Creature):  # Swap
                    current_player.active_creature = action
                    self._show_text(self.player, f"{current_player.display_name} swapped to {action.display_name}!")
                else:  # Skill
                    attacker = current_player.active_creature
                    defender = self.bot.active_creature if current_player == self.player else self.player.active_creature
                    self._execute_skill(attacker, defender, action)

                    if not self._handle_knocked_out(self.player):
                        self._show_text(self.player, "You lost!")
                        self._transition_to_scene("MainMenuScene")
                        return
                    if not self._handle_knocked_out(self.bot):
                        self._show_text(self.player, "You won!")
                        self._transition_to_scene("MainMenuScene")
                        return

    def _get_player_action(self, player: Player):
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
                return skill_choice.thing

            elif choice == swap_button:
                # Show available creatures
                available_creatures = [c for c in player.creatures 
                                    if c.hp > 0 and c != player.active_creature]
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                creature_choices = [SelectThing(c) for c in available_creatures]
                back_button = Button("Back")
                swap_choice = self._wait_for_choice(player, creature_choices + [back_button])
                
                if swap_choice == back_button:
                    continue
                return swap_choice.thing

    def _determine_turn_order(self, p1, p1_action, p2, p2_action):
        # Swaps always go first
        if isinstance(p1_action, Creature) and not isinstance(p2_action, Creature):
            return (p1, p1_action), (p2, p2_action)
        if isinstance(p2_action, Creature) and not isinstance(p1_action, Creature):
            return (p2, p2_action), (p1, p1_action)
            
        # Compare speeds
        if p1.active_creature.speed > p2.active_creature.speed:
            return (p1, p1_action), (p2, p2_action)
        elif p2.active_creature.speed > p1.active_creature.speed:
            return (p2, p2_action), (p1, p1_action)
        else:
            # Random if speeds are equal
            if random.random() < 0.5:
                return (p1, p1_action), (p2, p2_action)
            return (p2, p2_action), (p1, p1_action)
