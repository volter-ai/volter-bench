from mini_game_engine.engine.lib import AbstractGameScene, SelectThing, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = app.create_bot("basic_opponent")
        self.turn_actions = []

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        
        return f"""=== Battle ===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.bot.display_name}'s {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player turn
            if not self.handle_turn(self.player):
                return
            
            # Bot turn
            if not self.handle_turn(self.bot):
                return
            
            # Resolution phase
            self.resolve_turn()
            
            # Reset turn actions
            self.turn_actions = []

    def handle_turn(self, current_player):
        if self.check_knocked_out(current_player.active_creature):
            if not self.handle_forced_swap(current_player):
                self.end_battle(current_player == self.player)
                return False
                
        attack_button = Button("Attack")
        swap_button = Button("Swap")
        choice = self._wait_for_choice(current_player, [attack_button, swap_button])
        
        if choice == attack_button:
            skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
            back_button = Button("Back")
            skill_choice = self._wait_for_choice(current_player, skill_choices + [back_button])
            
            if skill_choice != back_button:
                self.turn_actions.append(("skill", current_player, skill_choice.thing))
                return True
            
        # Must be swap
        available_creatures = [
            creature for creature in current_player.creatures 
            if creature != current_player.active_creature and creature.hp > 0
        ]
        swap_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        swap_choice = self._wait_for_choice(current_player, swap_choices + [back_button])
        
        if swap_choice != back_button:
            self.turn_actions.append(("swap", current_player, swap_choice.thing))
            return True
            
        return self.handle_turn(current_player)

    def resolve_turn(self):
        # Handle swaps first
        for action_type, player, thing in self.turn_actions:
            if action_type == "swap":
                player.active_creature = thing
                self._show_text(self.player, f"{player.display_name} swapped to {thing.display_name}!")

        # Then handle skills
        skill_actions = [(p, t) for at, p, t in self.turn_actions if at == "skill"]
        if len(skill_actions) == 2:
            p1, s1 = skill_actions[0]
            p2, s2 = skill_actions[1]
            
            # Determine order
            if p1.active_creature.speed > p2.active_creature.speed:
                order = [(p1, s1), (p2, s2)]
            elif p2.active_creature.speed > p1.active_creature.speed:
                order = [(p2, s2), (p1, s1)]
            else:
                order = random.sample([(p1, s1), (p2, s2)], 2)
                
            for attacker, skill in order:
                defender = self.bot if attacker == self.player else self.player
                self.execute_skill(attacker, defender, skill)

    def execute_skill(self, attacker, defender, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage!")

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def check_knocked_out(self, creature):
        return creature.hp <= 0

    def handle_forced_swap(self, player):
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if not available_creatures:
            return False
            
        swap_choices = [SelectThing(creature) for creature in available_creatures]
        choice = self._wait_for_choice(player, swap_choices)
        player.active_creature = choice.thing
        self._show_text(self.player, f"{player.display_name} sent out {choice.thing.display_name}!")
        return True

    def end_battle(self, player_lost):
        if player_lost:
            self._show_text(self.player, "You lost the battle!")
        else:
            self._show_text(self.player, "You won the battle!")
            
        # Reset creature HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        self._transition_to_scene("MainMenuScene")
