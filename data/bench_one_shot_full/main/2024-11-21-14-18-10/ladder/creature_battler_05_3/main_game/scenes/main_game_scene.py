from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.initialize_creatures()

    def initialize_creatures(self):
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

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Get player actions
            p1_action = self.get_player_action(self.player)
            p2_action = self.get_player_action(self.bot)
            
            # Resolve actions
            self.resolve_turn(p1_action, p2_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

        self.initialize_creatures()  # Reset for next battle
        self._transition_to_scene("MainMenuScene")

    def get_player_action(self, player):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(player, [attack_button, swap_button])

            if choice == attack_button:
                skills = [SelectThing(s) for s in player.active_creature.skills]
                back_button = Button("Back")
                skill_choice = self._wait_for_choice(player, skills + [back_button])
                if skill_choice == back_button:
                    continue
                return {"type": "attack", "skill": skill_choice.thing}

            elif choice == swap_button:
                available_creatures = [
                    c for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                if not available_creatures:
                    self._show_text(player, "No other creatures available!")
                    continue
                    
                creatures = [SelectThing(c) for c in available_creatures]
                back_button = Button("Back")
                creature_choice = self._wait_for_choice(player, creatures + [back_button])
                if creature_choice == back_button:
                    continue
                return {"type": "swap", "creature": creature_choice.thing}

    def resolve_turn(self, p1_action, p2_action):
        # Handle swaps first
        for p, action in [(self.player, p1_action), (self.bot, p2_action)]:
            if action["type"] == "swap":
                p.active_creature = action["creature"]
                self._show_text(self.player, f"{p.display_name} swapped to {action['creature'].display_name}!")

        # Then handle attacks
        actions = [(self.player, p1_action), (self.bot, p2_action)]
        if p1_action["type"] == "attack" and p2_action["type"] == "attack":
            # Sort by speed
            actions.sort(key=lambda x: x[0].active_creature.speed, reverse=True)

        for attacker, action in actions:
            if action["type"] == "attack":
                defender = self.bot if attacker == self.player else self.player
                self.execute_attack(attacker, defender, action["skill"])

    def execute_attack(self, attacker, defender, skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = (attacker.active_creature.attack + 
                         skill.base_damage - 
                         defender.active_creature.defense)
        else:
            raw_damage = (skill.base_damage * 
                         attacker.active_creature.sp_attack / 
                         defender.active_creature.sp_defense)

        # Apply type effectiveness
        effectiveness = self.get_type_effectiveness(
            skill.skill_type, 
            defender.active_creature.creature_type
        )
        final_damage = int(raw_damage * effectiveness)
        
        # Apply damage
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        # Show result
        effectiveness_text = ""
        if effectiveness > 1:
            effectiveness_text = "It's super effective!"
        elif effectiveness < 1:
            effectiveness_text = "It's not very effective..."
            
        self._show_text(
            self.player,
            f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}! {effectiveness_text}"
        )

        # Handle fainting
        if defender.active_creature.hp <= 0:
            self._show_text(
                self.player,
                f"{defender.display_name}'s {defender.active_creature.display_name} fainted!"
            )
            self.handle_fainted_creature(defender)

    def get_type_effectiveness(self, skill_type, creature_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness_chart = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness_chart.get(skill_type, {}).get(creature_type, 1.0)

    def handle_fainted_creature(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return
            
        self._show_text(self.player, f"{player.display_name} must choose a new creature!")
        creatures = [SelectThing(c) for c in available_creatures]
        choice = self._wait_for_choice(player, creatures)
        player.active_creature = choice.thing

    def check_battle_end(self):
        for player in [self.player, self.bot]:
            if all(c.hp <= 0 for c in player.creatures):
                winner = self.bot if player == self.player else self.player
                self._show_text(self.player, f"{winner.display_name} wins!")
                return True
        return False
