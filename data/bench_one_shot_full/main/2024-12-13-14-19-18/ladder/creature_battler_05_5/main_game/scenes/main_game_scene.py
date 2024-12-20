from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Player
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self._reset_creatures()

    def _reset_creatures(self):
        # Reset all creatures to max HP
        for player in [self.player, self.bot]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
            player.active_creature = player.creatures[0]

    def __str__(self):
        p1 = self.player
        p2 = self.bot
        return f"""=== Battle ===
{p1.display_name}'s {p1.active_creature.display_name}: {p1.active_creature.hp}/{p1.active_creature.max_hp} HP
{p2.display_name}'s {p2.active_creature.display_name}: {p2.active_creature.hp}/{p2.active_creature.max_hp} HP

> Attack
> Swap
"""

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def _get_type_effectiveness(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def _handle_knocked_out(self, player: Player) -> bool:
        # Returns True if player has any creatures left
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return False
            
        if player.active_creature.hp <= 0:
            choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            
        return True

    def _get_player_action(self) -> tuple:
        while True:
            # Main choice level
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            back_button = Button("Back")
            choice = self._wait_for_choice(self.player, [attack_button, swap_button, back_button])
            
            if choice == back_button:
                return None

            if choice == attack_button:
                # Attack submenu
                skill_choices = [SelectThing(s) for s in self.player.active_creature.skills]
                skill_choices.append(Button("Back"))
                skill_choice = self._wait_for_choice(self.player, skill_choices)
                
                if isinstance(skill_choice, Button):  # Back was chosen
                    continue
                    
                return ("attack", skill_choice.thing)
            else:
                # Swap submenu
                available_creatures = [c for c in self.player.creatures if c.hp > 0 and c != self.player.active_creature]
                if available_creatures:
                    creature_choices = [SelectThing(c) for c in available_creatures]
                    creature_choices.append(Button("Back"))
                    creature_choice = self._wait_for_choice(self.player, creature_choices)
                    
                    if isinstance(creature_choice, Button):  # Back was chosen
                        continue
                        
                    return ("swap", creature_choice.thing)

    def _determine_turn_order(self, p1: Player, p2: Player) -> tuple[Player, Player]:
        p1_speed = p1.active_creature.speed
        p2_speed = p2.active_creature.speed
        
        if p1_speed > p2_speed:
            return (p1, p2)
        elif p2_speed > p1_speed:
            return (p2, p1)
        else:
            # Speed tie - random 50/50 chance
            return (p1, p2) if random.random() < 0.5 else (p2, p1)

    def run(self):
        while True:
            # Player turn
            player_action = self._get_player_action()
            if player_action is None:
                continue

            # Bot turn
            bot_action = None
            if random.random() < 0.8:  # 80% chance to attack
                bot_action = ("attack", random.choice(self.bot.active_creature.skills))
            else:
                available_creatures = [c for c in self.bot.creatures if c.hp > 0 and c != self.bot.active_creature]
                if available_creatures:
                    bot_action = ("swap", random.choice(available_creatures))
                else:
                    bot_action = ("attack", random.choice(self.bot.active_creature.skills))

            # Resolution phase
            # Handle swaps first
            if player_action[0] == "swap":
                self.player.active_creature = player_action[1]
            if bot_action[0] == "swap":
                self.bot.active_creature = bot_action[1]

            # Handle attacks based on speed
            if player_action[0] == "attack" and bot_action[0] == "attack":
                first, second = self._determine_turn_order(self.player, self.bot)
                first_action = player_action if first == self.player else bot_action
                second_action = bot_action if first == self.player else player_action

                # First attack
                damage = self._calculate_damage(first.active_creature, second.active_creature, first_action[1])
                second.active_creature.hp -= damage
                self._show_text(self.player, f"{first.active_creature.display_name} used {first_action[1].display_name} for {damage} damage!")

                # Second attack if still alive
                if second.active_creature.hp > 0:
                    damage = self._calculate_damage(second.active_creature, first.active_creature, second_action[1])
                    first.active_creature.hp -= damage
                    self._show_text(self.player, f"{second.active_creature.display_name} used {second_action[1].display_name} for {damage} damage!")

            # Check for knocked out creatures
            player_has_creatures = self._handle_knocked_out(self.player)
            bot_has_creatures = self._handle_knocked_out(self.bot)

            if not player_has_creatures:
                self._show_text(self.player, "You lost!")
                break
            elif not bot_has_creatures:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")
