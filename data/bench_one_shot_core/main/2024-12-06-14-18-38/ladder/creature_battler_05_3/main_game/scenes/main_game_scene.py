from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature
import random

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

Actions:
> Attack
> Swap
"""

    def run(self):
        while True:
            # Player phase
            player_action = self.get_player_action(self.player)
            if not player_action:
                return
                
            # Bot phase
            bot_action = self.get_player_action(self.bot)
            if not bot_action:
                return

            # Resolution phase
            self.resolve_actions(player_action, bot_action)

            # Check for battle end
            if self.check_battle_end():
                return

    def get_player_action(self, player: Player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(player, [attack_button, swap_button])

            if choice == attack_button:
                # Show skills
                skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skill_choices + [back_button])
                
                if skill_choice == back_button:
                    continue
                    
                return {"type": "attack", "skill": skill_choice.thing}

            elif choice == swap_button:
                # Show available creatures
                available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                creature_choices = [SelectThing(creature) for creature in available_creatures]
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, creature_choices + [back_button])
                
                if creature_choice == back_button:
                    continue
                    
                return {"type": "swap", "creature": creature_choice.thing}

    def resolve_actions(self, p1_action, p2_action):
        # Handle swaps first
        for p, action in [(self.player, p1_action), (self.bot, p2_action)]:
            if action["type"] == "swap":
                p.active_creature = action["creature"]
                self._show_text(self.player, f"{p.display_name} swapped to {action['creature'].display_name}!")

        # Then handle attacks
        actions = [(self.player, p1_action), (self.bot, p2_action)]
        
        # Sort by speed for attacks
        actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
        if actions[0][0].active_creature.speed == actions[1][0].active_creature.speed:
            random.shuffle(actions)

        for attacker, action in actions:
            if action["type"] == "attack":
                defender = self.bot if attacker == self.player else self.player
                self.execute_attack(attacker, defender, action["skill"])

    def execute_attack(self, attacker: Player, defender: Player, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Type effectiveness
        effectiveness = self.get_type_effectiveness(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * effectiveness)

        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage!")

        # Handle KO
        if defender.active_creature.hp <= 0:
            self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} was knocked out!")
            self.handle_knockout(defender)

    def get_type_effectiveness(self, skill_type: str, defender_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, player: Player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        self._show_text(player, "Choose next creature:")
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, creature_choices)
        player.active_creature = choice.thing
        self._show_text(self.player, f"{player.display_name} sent out {choice.thing.display_name}!")

    def check_battle_end(self) -> bool:
        for player in [self.player, self.bot]:
            if all(c.hp <= 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                self._transition_to_scene("MainMenuScene")
                return True
        return False
