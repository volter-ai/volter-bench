from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature, Player

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
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

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_actions(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

        # Reset creatures
        for p in [self.player, self.bot]:
            for c in p.creatures:
                c.hp = c.max_hp
            p.active_creature = None

        self._transition_to_scene("MainMenuScene")

    def get_player_action(self, player):
        while True:
            attack = Button("Attack")
            swap = Button("Swap")
            choice = self._wait_for_choice(player, [attack, swap])

            if choice == attack:
                skills = [Button(s.display_name) for s in player.active_creature.skills]
                back = Button("Back")
                skill_choice = self._wait_for_choice(player, skills + [back])
                if skill_choice != back:
                    return ("attack", skill_choice.display_name.lower())
            
            elif choice == swap:
                available = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
                if available:
                    creatures = [SelectThing(c) for c in available]
                    back = Button("Back")
                    swap_choice = self._wait_for_choice(player, creatures + [back])
                    if swap_choice != back:
                        return ("swap", swap_choice.thing)

    def resolve_actions(self, p_action, b_action):
        # Handle swaps first
        if p_action[0] == "swap":
            self.player.active_creature = p_action[1]
        if b_action[0] == "swap":
            self.bot.active_creature = b_action[1]

        # Then handle attacks
        first = self.player if self.player.active_creature.speed >= self.bot.active_creature.speed else self.bot
        second = self.bot if first == self.player else self.player
        first_action = p_action if first == self.player else b_action
        second_action = b_action if first == self.player else p_action

        if first_action[0] == "attack":
            self.execute_attack(first, second, first_action[1])
        if second.active_creature.hp > 0 and second_action[0] == "attack":
            self.execute_attack(second, first, second_action[1])

    def execute_attack(self, attacker, defender, skill_name):
        skill = next(s for s in attacker.active_creature.skills if s.prototype_id == skill_name)
        target = defender.active_creature

        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - target.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / target.sp_defense) * skill.base_damage

        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, target.creature_type)
        final_damage = int(raw_damage * effectiveness)
        
        target.hp = max(0, target.hp - final_damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{target.display_name} took {final_damage} damage!")

        if target.hp == 0:
            self.handle_knockout(defender)

    def get_type_effectiveness(self, skill_type, target_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(target_type, 1.0)

    def handle_knockout(self, player):
        self._show_text(player, f"{player.active_creature.display_name} was knocked out!")
        available = [c for c in player.creatures if c.hp > 0]
        if available:
            choices = [SelectThing(c) for c in available]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(player, f"Go, {player.active_creature.display_name}!")

    def check_battle_end(self):
        p_alive = any(c.hp > 0 for c in self.player.creatures)
        b_alive = any(c.hp > 0 for c in self.bot.creatures)
        
        if not p_alive or not b_alive:
            winner = self.player if p_alive else self.bot
            self._show_text(self.player, f"{winner.display_name} wins!")
            return True
        return False
