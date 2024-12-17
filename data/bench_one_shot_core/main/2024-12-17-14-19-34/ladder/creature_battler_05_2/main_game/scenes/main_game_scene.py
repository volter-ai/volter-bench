from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
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
> Swap"""

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Calculate type effectiveness
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

    def _handle_player_turn(self, player: Player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        
        choice = self._wait_for_choice(player, [attack_button, swap_button])
        
        if choice == attack_button:
            # Show skills
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            back_button = Button("Back")
            skill_choice = self._wait_for_choice(player, skill_choices + [back_button])
            
            if skill_choice == back_button:
                return self._handle_player_turn(player)
            return ("attack", skill_choice.thing)
        else:
            # Show available creatures
            available_creatures = [c for c in player.creatures if c.hp > 0 and c != player.active_creature]
            if not available_creatures:
                return self._handle_player_turn(player)
                
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            back_button = Button("Back")
            creature_choice = self._wait_for_choice(player, creature_choices + [back_button])
            
            if creature_choice == back_button:
                return self._handle_player_turn(player)
            return ("swap", creature_choice.thing)

    def _check_game_over(self):
        for player in [self.player, self.bot]:
            if all(c.hp <= 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                self._transition_to_scene("MainMenuScene")
                return True
        return False

    def _force_swap(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return False
            
        if len(available_creatures) == 1:
            player.active_creature = available_creatures[0]
        else:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = choice.thing
        return True

    def run(self):
        while True:
            # Player turns
            p1_action = self._handle_player_turn(self.player)
            p2_action = self._handle_player_turn(self.bot)

            # Resolution phase
            players = [(self.player, p1_action), (self.bot, p2_action)]
            
            # Handle swaps first
            for player, action in players:
                if action[0] == "swap":
                    player.active_creature = action[1]
                    self._show_text(self.player, f"{player.display_name} swapped to {action[1].display_name}!")

            # Then handle attacks in speed order
            attack_players = [(p, a) for p, a in players if a[0] == "attack"]
            attack_players.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
            
            for player, action in attack_players:
                if player.active_creature.hp <= 0:
                    continue
                    
                opponent = self.bot if player == self.player else self.player
                skill = action[1]
                
                damage = self._calculate_damage(player.active_creature, opponent.active_creature, skill)
                opponent.active_creature.hp -= damage
                
                self._show_text(self.player, 
                    f"{player.display_name}'s {player.active_creature.display_name} used {skill.display_name}! "
                    f"Dealt {damage} damage!")

                if opponent.active_creature.hp <= 0:
                    self._show_text(self.player, 
                        f"{opponent.display_name}'s {opponent.active_creature.display_name} was knocked out!")
                    if not self._force_swap(opponent):
                        break

            if self._check_game_over():
                break
