from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self._initialize_creatures()

    def _initialize_creatures(self):
        # Reset creatures to starting state
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

    def _get_damage_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == defender_type or skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _calculate_damage(self, attacker: Creature, defender: Creature, skill) -> int:
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        multiplier = self._get_damage_multiplier(skill.skill_type, defender.creature_type)
        return int(raw_damage * multiplier)

    def _execute_turn(self, p1_action, p2_action):
        # Handle swaps first
        for action, player in [(p1_action, self.player), (p2_action, self.bot)]:
            if isinstance(action, Creature):
                player.active_creature = action
                self._show_text(player, f"{player.display_name} swapped to {action.display_name}!")

        # Then handle attacks
        actions = [(p1_action, self.player, self.bot), (p2_action, self.bot, self.player)]
        # Sort by speed
        actions.sort(key=lambda x: x[1].active_creature.speed, reverse=True)

        for action, attacker, defender in actions:
            if isinstance(action, Creature):
                continue
                
            damage = self._calculate_damage(attacker.active_creature, defender.active_creature, action)
            defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
            self._show_text(attacker, f"{attacker.active_creature.display_name} used {action.display_name}!")
            self._show_text(defender, f"{defender.active_creature.display_name} took {damage} damage!")

    def _handle_fainted(self, player: Player) -> bool:
        if player.active_creature.hp > 0:
            return False

        self._show_text(player, f"{player.active_creature.display_name} fainted!")
        available = [c for c in player.creatures if c.hp > 0]
        
        if not available:
            return True
            
        choices = [SelectThing(c) for c in available]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return False

    def run(self):
        while True:
            # Player turn
            attack = Button("Attack")
            swap = Button("Swap")
            choice = self._wait_for_choice(self.player, [attack, swap])

            p1_action = self.player.active_creature.skills[0]  # Default to first skill
            if choice == attack:
                skill_choices = [SelectThing(s) for s in self.player.active_creature.skills]
                p1_action = self._wait_for_choice(self.player, skill_choices).thing
            elif choice == swap:
                available = [c for c in self.player.creatures if c.hp > 0 and c != self.player.active_creature]
                if available:
                    swap_choices = [SelectThing(c) for c in available]
                    p1_action = self._wait_for_choice(self.player, swap_choices).thing

            # Bot turn
            p2_action = self.bot.active_creature.skills[0]  # Simple bot just uses first skill

            # Execute turn
            self._execute_turn(p1_action, p2_action)

            # Check for fainted creatures
            if self._handle_fainted(self.player):
                self._show_text(self.player, "You lost!")
                break
            if self._handle_fainted(self.bot):
                self._show_text(self.player, "You won!")
                break

        self._initialize_creatures()
        self._transition_to_scene("MainMenuScene")
