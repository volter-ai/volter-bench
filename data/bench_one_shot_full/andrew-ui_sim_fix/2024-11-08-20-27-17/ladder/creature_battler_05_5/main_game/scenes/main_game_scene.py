from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        
        # Initialize creatures
        for p in [self.player, self.bot]:
            p.active_creature = p.creatures[0]
            for c in p.creatures:
                c.hp = c.max_hp

    def __str__(self):
        p_creature = self.player.active_creature
        b_creature = self.bot.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {b_creature.display_name}: {b_creature.hp}/{b_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                self._quit_whole_game()  # <-- This is the fix: explicitly quit the game when battle ends

    def get_player_action(self, player: Player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(player, [attack_button, swap_button])

            if choice == attack_button:
                skills = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skills + [back_button])
                if skill_choice != back_button:
                    return ("attack", skill_choice.thing)
            else:
                available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
                if available_creatures:
                    creatures = [SelectThing(creature) for creature in available_creatures]
                    back_button = Button("Back")
                    creature_choice = self._wait_for_choice(player, creatures + [back_button])
                    if creature_choice != back_button:
                        return ("swap", creature_choice.thing)

    def resolve_turn(self, player_action, bot_action):
        actions = [(self.player, player_action), (self.bot, bot_action)]
        
        # Sort by speed for attacks
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        
        # Execute swaps first
        for player, action in actions:
            if action[0] == "swap":
                player.active_creature = action[1]
                self._show_text(player, f"{player.display_name} swapped to {action[1].display_name}!")

        # Then execute attacks
        for player, action in actions:
            if action[0] == "attack":
                target = self.bot if player == self.player else self.player
                self.execute_attack(player, target, action[1])
                
                # Force swap if creature fainted
                if target.active_creature.hp <= 0:
                    available = [c for c in target.creatures if c.hp > 0]
                    if available:
                        choices = [SelectThing(c) for c in available]
                        swap_to = self._wait_for_choice(target, choices).thing
                        target.active_creature = swap_to
                        self._show_text(target, f"{target.display_name} sent out {swap_to.display_name}!")

    def execute_attack(self, attacker: Player, defender: Player, skill):
        # Calculate damage
        raw_damage = self.calculate_raw_damage(attacker.active_creature, defender.active_creature, skill)
        type_factor = self.get_type_factor(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * type_factor)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"It dealt {final_damage} damage!")

    def calculate_raw_damage(self, attacker: Creature, defender: Creature, skill):
        if skill.is_physical:
            return skill.base_damage + attacker.attack - defender.defense
        else:
            return (attacker.sp_attack / defender.sp_defense) * skill.base_damage

    def get_type_factor(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def check_battle_end(self) -> bool:
        for player in [self.player, self.bot]:
            if all(c.hp <= 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                return True
        return False
