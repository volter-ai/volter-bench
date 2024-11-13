from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from main_game.models import Player, Creature

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")
        self.turn_actions = []
        
        # Reset creatures
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.bot.creatures:
            creature.hp = creature.max_hp
            
        # Set initial active creatures
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
Your {self.player.active_creature.display_name}: {self.player.active_creature.hp}/{self.player.active_creature.max_hp} HP
Foe's {self.bot.active_creature.display_name}: {self.bot.active_creature.hp}/{self.bot.active_creature.max_hp} HP

> Attack
> Swap
"""

    def run(self):
        while True:
            # Player turn
            if not self.handle_turn(self.player):
                return
            
            # Bot turn
            if not self.handle_turn(self.bot):
                return
                
            # Resolution phase
            self.resolve_turn()
            
            # Check for battle end
            if self.check_battle_end():
                return

    def handle_turn(self, current_player: Player) -> bool:
        """Returns False if battle should end"""
        if current_player.active_creature.hp <= 0:
            available_creatures = [c for c in current_player.creatures if c.hp > 0]
            if not available_creatures:
                return False
            
            choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(current_player, choices)
            current_player.active_creature = choice.thing
            return True

        while True:  # Main action menu loop
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choice = self._wait_for_choice(current_player, [attack_button, swap_button])

            if choice == attack_button:
                # Attack submenu
                skill_choices = [SelectThing(s) for s in current_player.active_creature.skills]
                back_button = Button("Back")
                skill_choices.append(back_button)
                
                skill_choice = self._wait_for_choice(current_player, skill_choices)
                if skill_choice == back_button:
                    continue  # Go back to main action menu
                    
                self.turn_actions.append(("attack", current_player, skill_choice.thing))
                break  # Exit action menu after valid choice
                
            else:  # Swap chosen
                available_creatures = [c for c in current_player.creatures if c.hp > 0 and c != current_player.active_creature]
                if available_creatures:
                    swap_choices = [SelectThing(c) for c in available_creatures]
                    back_button = Button("Back")
                    swap_choices.append(back_button)
                    
                    swap_choice = self._wait_for_choice(current_player, swap_choices)
                    if swap_choice == back_button:
                        continue  # Go back to main action menu
                        
                    self.turn_actions.append(("swap", current_player, swap_choice.thing))
                    break  # Exit action menu after valid choice
                else:
                    self._show_text(current_player, "No other creatures available to swap!")
                    continue  # Go back to main action menu

        return True

    def resolve_turn(self):
        # Handle swaps first
        for action_type, player, thing in self.turn_actions:
            if action_type == "swap":
                player.active_creature = thing
                
        # Then handle attacks
        attacks = [(p, s) for t, p, s in self.turn_actions if t == "attack"]
        if len(attacks) == 2:
            # Sort by speed
            attacks.sort(key=lambda x: x[0].active_creature.speed, reverse=True)
            
        for attacker, skill in attacks:
            defender = self.bot if attacker == self.player else self.player
            self.execute_attack(attacker, defender, skill)
            
        self.turn_actions = []

    def execute_attack(self, attacker: Player, defender: Player, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage
            
        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender, f"{defender.active_creature.display_name} took {final_damage} damage!")

    def get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        bot_has_creatures = any(c.hp > 0 for c in self.bot.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif not bot_has_creatures:
            self._show_text(self.player, "You won the battle!")
            self._transition_to_scene("MainMenuScene") 
            return True
            
        return False
