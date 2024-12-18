from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Creature

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
> Swap"""

    def run(self):
        while True:
            # Force swap if active creature is knocked out
            for player in [self.player, self.bot]:
                if player.active_creature.hp <= 0:
                    if not self.force_swap(player):
                        winner = self.bot if player == self.player else self.player
                        self._show_text(self.player, f"{winner.display_name} wins!")
                        self._quit_whole_game()  # Properly end the game instead of returning
                        return  # Return after _quit_whole_game to prevent further execution

            # Get actions
            player_action = self.get_player_action(self.player)
            if not player_action:  # Back button pressed
                continue
                
            bot_action = self.get_player_action(self.bot)
            
            # Execute actions
            self.resolve_turn(player_action, bot_action)

    def force_swap(self, player):
        """Forces player to swap when active creature is knocked out. Returns False if no valid creatures."""
        valid_creatures = [c for c in player.creatures if c.hp > 0]
        if not valid_creatures:
            return False
            
        choices = [SelectThing(creature) for creature in valid_creatures]
        choice = self._wait_for_choice(player, choices)
        player.active_creature = choice.thing
        return True

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            
            choice = self._wait_for_choice(player, [attack_button, swap_button])
            
            if choice == attack_button:
                back_button = Button("Back")
                choices = [SelectThing(skill) for skill in player.active_creature.skills]
                choices.append(back_button)
                
                action = self._wait_for_choice(player, choices)
                if action == back_button:
                    continue
                return action
            else:
                back_button = Button("Back")
                valid_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
                choices = [SelectThing(creature) for creature in valid_creatures]
                
                if choices:  # Only add back button if there are swap choices
                    choices.append(back_button)
                    action = self._wait_for_choice(player, choices)
                    if action == back_button:
                        continue
                    return action
                else:
                    self._show_text(player, "No creatures available to swap!")
                    continue

    def resolve_turn(self, p1_action, p2_action):
        # Handle swaps first
        for action in [p1_action, p2_action]:
            if isinstance(action.thing, Creature):
                player = self.player if action.thing in self.player.creatures else self.bot
                player.active_creature = action.thing
                
        # Then handle attacks in speed order
        actions = [(p1_action, self.player), (p2_action, self.bot)]
        actions.sort(key=lambda x: x[1].active_creature.speed, reverse=True)
        
        for action, attacker in actions:
            if not isinstance(action.thing, Creature):
                defender = self.bot if attacker == self.player else self.player
                self.execute_skill(action.thing, attacker.active_creature, defender.active_creature)

    def execute_skill(self, skill, attacker, defender):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.hp = max(0, defender.hp - final_damage)
        self._show_text(self.player, f"{attacker.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"Dealt {final_damage} damage!")

    def get_type_multiplier(self, attack_type, defend_type):
        if attack_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(attack_type, {}).get(defend_type, 1.0)
