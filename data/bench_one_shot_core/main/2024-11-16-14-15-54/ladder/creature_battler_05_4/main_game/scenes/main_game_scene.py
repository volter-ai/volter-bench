from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self._reset_creatures()

    def _reset_creatures(self):
        # Reset all creatures to full HP
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

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
            
        return int(raw_damage * effectiveness)

    def _get_available_creatures(self, player: Player):
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def _handle_fainted(self, player: Player):
        available = self._get_available_creatures(player)
        if not available:
            return False
            
        choices = [SelectThing(c) for c in available]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return True

    def _execute_turn(self, first_player, first_action, second_player, second_action):
        # Handle swaps first
        for player, action in [(first_player, first_action), (second_player, second_action)]:
            if isinstance(action, Creature):
                player.active_creature = action
                self._show_text(self.player, f"{player.display_name} swapped to {action.display_name}!")

        # Then handle attacks
        for attacker, action in [(first_player, first_action), (second_player, second_action)]:
            if isinstance(action, Creature):
                continue
                
            defender = second_player if attacker == first_player else first_player
            damage = self._calculate_damage(attacker.active_creature, defender.active_creature, action)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            
            self._show_text(self.player, 
                f"{attacker.display_name}'s {attacker.active_creature.display_name} used {action.display_name}!")
            self._show_text(self.player,
                f"{defender.display_name}'s {defender.active_creature.display_name} took {damage} damage!")
            
            if defender.active_creature.hp == 0:
                self._show_text(self.player,
                    f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
                if not self._handle_fainted(defender):
                    return defender
                    
        return None

    def run(self):
        while True:
            # Player turn
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(self.player, [attack_button, swap_button])
            
            player_action = None
            if choice == attack_button:
                skill_choices = [SelectThing(s) for s in self.player.active_creature.skills]
                player_action = self._wait_for_choice(self.player, skill_choices).thing
            else:
                creature_choices = [SelectThing(c) for c in self._get_available_creatures(self.player)]
                if creature_choices:
                    player_action = self._wait_for_choice(self.player, creature_choices).thing
                else:
                    continue

            # Bot turn
            if random.random() < 0.2 and self._get_available_creatures(self.bot):  # 20% chance to swap
                bot_action = random.choice(self._get_available_creatures(self.bot))
            else:
                bot_action = random.choice(self.bot.active_creature.skills)

            # Determine turn order
            if (isinstance(player_action, Creature) or isinstance(bot_action, Creature) or
                self.player.active_creature.speed == self.bot.active_creature.speed):
                first_player = random.choice([self.player, self.bot])
            else:
                first_player = (self.player if self.player.active_creature.speed > 
                              self.bot.active_creature.speed else self.bot)
                              
            second_player = self.bot if first_player == self.player else self.player
            first_action = player_action if first_player == self.player else bot_action
            second_action = bot_action if first_player == self.player else player_action

            # Execute turn
            loser = self._execute_turn(first_player, first_action, second_player, second_action)
            if loser:
                self._show_text(self.player, 
                    f"{'You won!' if loser == self.bot else 'You lost!'}")
                self._transition_to_scene("MainMenuScene")
                return
