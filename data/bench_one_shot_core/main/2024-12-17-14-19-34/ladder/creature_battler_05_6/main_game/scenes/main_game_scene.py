from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self._reset_creatures()

    def _reset_creatures(self):
        # Reset all creatures to full HP
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

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        # Calculate type effectiveness
        effectiveness = self._get_type_effectiveness(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * effectiveness)

    def _get_type_effectiveness(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"water": 0.5, "leaf": 2.0},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def _get_player_action(self, player: Player):
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
            else:
                available_creatures = [
                    SelectThing(c) for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                if not available_creatures:
                    continue
                available_creatures.append(Button("Back"))
                creature_choice = self._wait_for_choice(player, available_creatures)
                if isinstance(creature_choice, Button):
                    continue
                return ("swap", creature_choice.thing)

    def _force_swap(self, player: Player):
        available_creatures = [
            SelectThing(c) for c in player.creatures 
            if c.hp > 0 and c != player.active_creature
        ]
        if not available_creatures:
            return False
        
        choice = self._wait_for_choice(player, available_creatures)
        player.active_creature = choice.thing
        return True

    def run(self):
        while True:
            # Get actions
            p1_action = self._get_player_action(self.player)
            p2_action = self._get_player_action(self.bot)

            # Determine order
            if p1_action[0] == "swap" and p2_action[0] == "swap":
                order = [(self.player, p1_action), (self.bot, p2_action)]
            elif p1_action[0] == "swap":
                order = [(self.player, p1_action), (self.bot, p2_action)]
            elif p2_action[0] == "swap":
                order = [(self.bot, p2_action), (self.player, p1_action)]
            else:
                # Both attacking - use speed
                if self.player.active_creature.speed > self.bot.active_creature.speed:
                    order = [(self.player, p1_action), (self.bot, p2_action)]
                elif self.bot.active_creature.speed > self.player.active_creature.speed:
                    order = [(self.bot, p2_action), (self.player, p1_action)]
                else:
                    order = random.sample([(self.player, p1_action), (self.bot, p2_action)], 2)

            # Execute actions
            for player, (action_type, action) in order:
                if action_type == "swap":
                    player.active_creature = action
                    self._show_text(player, f"{player.display_name} swapped to {action.display_name}!")
                else:
                    target = self.bot if player == self.player else self.player
                    damage = self._calculate_damage(player.active_creature, target.active_creature, action)
                    target.active_creature.hp -= damage
                    self._show_text(player, f"{player.active_creature.display_name} used {action.display_name} for {damage} damage!")

                    if target.active_creature.hp <= 0:
                        target.active_creature.hp = 0
                        self._show_text(target, f"{target.active_creature.display_name} was knocked out!")
                        if not self._force_swap(target):
                            self._show_text(self.player, 
                                "You win!" if target == self.bot else "You lose!")
                            self._transition_to_scene("MainMenuScene")
                            return
