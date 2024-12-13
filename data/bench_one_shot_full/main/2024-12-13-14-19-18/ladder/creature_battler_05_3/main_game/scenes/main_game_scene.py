from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random
from typing import List, Tuple
from main_game.models import Player, Creature, Skill

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

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
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
            "fire": {"water": 0.5, "leaf": 2.0},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def _get_available_creatures(self, player: Player) -> List[Creature]:
        return [c for c in player.creatures if c.hp > 0 and c != player.active_creature]

    def _handle_turn(self, p1: Player, p2: Player) -> Tuple[str, str]:
        # Get actions from both players
        p1_action = self._get_player_action(p1)
        p2_action = self._get_player_action(p2)

        # Determine order
        if isinstance(p1_action, Creature) or isinstance(p2_action, Creature):
            # Swaps go first
            if isinstance(p1_action, Creature):
                p1.active_creature = p1_action
            if isinstance(p2_action, Creature):
                p2.active_creature = p2_action
        else:
            # Skills - determine order by speed
            if p1.active_creature.speed > p2.active_creature.speed:
                first, second = (p1, p1_action), (p2, p2_action)
            elif p2.active_creature.speed > p1.active_creature.speed:
                first, second = (p2, p2_action), (p1, p1_action)
            else:
                # Random if speeds are equal
                if random.random() < 0.5:
                    first, second = (p1, p1_action), (p2, p2_action)
                else:
                    first, second = (p2, p2_action), (p1, p1_action)

            # Execute skills
            for attacker, skill in [first, second]:
                if isinstance(skill, Skill):
                    defender = p2 if attacker == p1 else p1
                    damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
                    defender.active_creature.hp = max(0, defender.active_creature.hp - damage)

    def _get_player_action(self, player: Player):
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        back_button = Button("Back")

        while True:
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                # Show skills
                skill_choices = [SelectThing(s) for s in player.active_creature.skills]
                skill_choices.append(back_button)
                skill_choice = self._wait_for_choice(player, skill_choices)
                
                if skill_choice != back_button:
                    return skill_choice.thing
                    
            elif choice == swap_button:
                # Show available creatures
                available = self._get_available_creatures(player)
                if available:
                    creature_choices = [SelectThing(c) for c in available]
                    creature_choices.append(back_button)
                    creature_choice = self._wait_for_choice(player, creature_choices)
                    
                    if creature_choice != back_button:
                        return creature_choice.thing

    def run(self):
        while True:
            # Main battle loop
            self._handle_turn(self.player, self.bot)
            
            # Check for fainted creatures
            for p in [self.player, self.bot]:
                if p.active_creature.hp == 0:
                    available = self._get_available_creatures(p)
                    if available:
                        self._show_text(p, f"{p.active_creature.display_name} fainted! Choose a new creature!")
                        creature_choices = [SelectThing(c) for c in available]
                        p.active_creature = self._wait_for_choice(p, creature_choices).thing
                    else:
                        # Game over
                        winner = self.bot if p == self.player else self.player
                        self._show_text(self.player, f"Game Over! {winner.display_name} wins!")
                        self._transition_to_scene("MainMenuScene")
                        return
