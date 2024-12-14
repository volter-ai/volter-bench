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
        p1 = self.player
        p2 = self.bot
        
        return f"""=== Battle ===
{p1.display_name}'s {p1.active_creature.display_name}: {p1.active_creature.hp}/{p1.active_creature.max_hp} HP
{p2.display_name}'s {p2.active_creature.display_name}: {p2.active_creature.hp}/{p2.active_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            bot_action = self.get_player_action(self.bot)
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                # Reset creatures before quitting
                for p in [self.player, self.bot]:
                    for c in p.creatures:
                        c.hp = c.max_hp
                    p.active_creature = None
                self._quit_whole_game()  # <-- Added this line to properly end the game
                return

    def get_player_action(self, player: Player):
        while True:
            attack = Button("Attack")
            swap = Button("Swap")
            choice = self._wait_for_choice(player, [attack, swap])

            if choice == attack:
                skills = [Button(s.display_name) for s in player.active_creature.skills]
                back = Button("Back")
                skill_choice = self._wait_for_choice(player, skills + [back])
                if skill_choice != back:
                    return ("attack", skill_choice.display_name)
            
            elif choice == swap:
                available = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
                if available:
                    creatures = [SelectThing(c) for c in available]
                    back = Button("Back")
                    swap_choice = self._wait_for_choice(player, creatures + [back])
                    if swap_choice != back:
                        return ("swap", swap_choice.thing)

    def resolve_turn(self, p1_action, p2_action):
        # Handle swaps first
        for player, action in [(self.player, p1_action), (self.bot, p2_action)]:
            if action[0] == "swap":
                player.active_creature = action[1]
                self._show_text(player, f"{player.display_name} swapped to {action[1].display_name}!")

        # Then handle attacks
        actions = [(self.player, p1_action), (self.bot, p2_action)]
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)

        for attacker, action in actions:
            if action[0] == "attack":
                defender = self.bot if attacker == self.player else self.player
                skill = next(s for s in attacker.active_creature.skills if s.display_name == action[1])
                
                # Calculate damage
                if skill.is_physical:
                    raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
                else:
                    raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

                # Apply type effectiveness
                factor = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
                final_damage = int(raw_damage * factor)
                
                defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
                self._show_text(attacker, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
                self._show_text(defender, f"{defender.active_creature.display_name} took {final_damage} damage!")

                # Force swap if knocked out
                if defender.active_creature.hp == 0:
                    available = [c for c in defender.creatures if c.hp > 0]
                    if available:
                        choices = [SelectThing(c) for c in available]
                        swap_choice = self._wait_for_choice(defender, choices)
                        defender.active_creature = swap_choice.thing
                        self._show_text(defender, f"{defender.display_name} sent out {swap_choice.thing.display_name}!")

    def get_type_effectiveness(self, skill_type: str, target_type: str) -> float:
        if skill_type == target_type or skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(target_type, 1.0)

    def check_battle_end(self) -> bool:
        for player in [self.player, self.bot]:
            if all(c.hp == 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                return True
        return False
