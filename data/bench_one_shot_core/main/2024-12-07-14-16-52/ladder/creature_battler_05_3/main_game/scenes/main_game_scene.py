from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing, DictionaryChoice
from main_game.models import Creature, Skill
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.game_over = False
        
        # Initialize creatures
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = p.creatures[0]

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

Your other creatures:
{self._format_bench(self.player)}

Foe's other creatures:
{self._format_bench(self.bot)}
"""

    def _format_bench(self, player):
        return "\n".join(f"- {c.display_name}: {c.hp}/{c.max_hp} HP" 
                        for c in player.creatures 
                        if c != player.active_creature)

    def run(self):
        while not self.game_over:
            # Battle loop
            p_action = self._get_player_action(self.player)
            b_action = self._get_player_action(self.bot)
            
            self._resolve_actions(p_action, b_action)
            
            # Check for battle end
            self._check_battle_end()
            
        # Game is over, so quit
        self._quit_whole_game()

    def _get_player_action(self, player):
        while True:
            choice = self._wait_for_choice(player, [
                Button("Attack"),
                Button("Swap"),
            ])
            
            if choice.display_name == "Attack":
                # Create SelectThing choices for skills with their display names as labels
                skills = [SelectThing(s, label=s.display_name) for s in player.active_creature.skills]
                skills.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skills)
                
                # For Button choices, check display_name; for SelectThing choices, check label
                if isinstance(skill_choice, Button):
                    if skill_choice.display_name != "Back":
                        return {"type": "attack", "skill": skill_choice.thing}
                else:  # SelectThing
                    return {"type": "attack", "skill": skill_choice.thing}
                
            else:  # Swap
                # Create SelectThing choices for creatures with their display names as labels
                available = [
                    SelectThing(c, label=c.display_name) 
                    for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                available.append(Button("Back"))
                swap_choice = self._wait_for_choice(player, available)
                
                # For Button choices, check display_name; for SelectThing choices, check label
                if isinstance(swap_choice, Button):
                    if swap_choice.display_name != "Back":
                        return {"type": "swap", "creature": swap_choice.thing}
                else:  # SelectThing
                    return {"type": "swap", "creature": swap_choice.thing}

    def _resolve_actions(self, p_action, b_action):
        # Handle swaps first
        if p_action["type"] == "swap":
            self.player.active_creature = p_action["creature"]
        if b_action["type"] == "swap":
            self.bot.active_creature = b_action["creature"]
            
        # Then handle attacks
        actions = []
        if p_action["type"] == "attack":
            actions.append((self.player, self.bot, p_action["skill"]))
        if b_action["type"] == "attack":
            actions.append((self.bot, self.player, b_action["skill"]))
            
        # Sort by speed
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        if len(actions) == 2 and actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
            random.shuffle(actions)
            
        # Execute attacks
        for attacker, defender, skill in actions:
            if defender.active_creature.hp <= 0:
                continue
                
            damage = self._calculate_damage(attacker.active_creature, defender.active_creature, skill)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            
            self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
            self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")
            
            if defender.active_creature.hp <= 0:
                self._handle_knockout(defender)

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill: Skill) -> int:
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
        return int(raw_damage * multiplier)

    def _get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _handle_knockout(self, player):
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        
        available = [c for c in player.creatures if c.hp > 0]
        if available:
            choices = [SelectThing(c, label=c.display_name) for c in available]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(player, f"Go, {player.active_creature.display_name}!")

    def _check_battle_end(self):
        p_alive = any(c.hp > 0 for c in self.player.creatures)
        b_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_alive or not b_alive:
            winner = self.player if p_alive else self.bot
            self._show_text(self.player, 
                          "You won!" if winner == self.player else "You lost!")
            self.game_over = True
