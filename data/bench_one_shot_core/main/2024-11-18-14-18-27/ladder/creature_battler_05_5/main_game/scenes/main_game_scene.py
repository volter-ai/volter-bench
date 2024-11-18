from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
from typing import Tuple, Union, Literal
from main_game.models import Skill, Creature

ActionType = Tuple[Literal["attack", "swap"], Union[Skill, Creature]]

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        
    def __str__(self):
        p_creature = self.player.active_creature
        o_creature = self.opponent.active_creature
        
        return f"""=== Battle ===
Your {p_creature.display_name}: {p_creature.hp}/{p_creature.max_hp} HP
Foe's {o_creature.display_name}: {o_creature.hp}/{o_creature.max_hp} HP

> Attack
> Swap"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player turn
            player_action = self.get_player_action(self.player)
            # Bot turn  
            bot_action = self.get_player_action(self.opponent)
            
            # Resolve actions
            self.resolve_turn(player_action, bot_action)
            
            # Check for battle end
            if self.check_battle_end():
                break

    def get_player_action(self, player) -> ActionType:
        while True:
            choice = self._wait_for_choice(player, [
                Button("Attack"),
                Button("Swap"),
            ])

            if isinstance(choice, Button) and choice.display_name == "Attack":
                skills = [SelectThing(skill) for skill in player.active_creature.skills]
                skills.append(Button("Back"))
                skill_choice = self._wait_for_choice(player, skills)
                
                if isinstance(skill_choice, Button):
                    continue  # Back button pressed
                else:
                    return ("attack", skill_choice.thing)
            else:
                available_creatures = [
                    SelectThing(c) for c in player.creatures 
                    if c != player.active_creature and c.hp > 0
                ]
                available_creatures.append(Button("Back"))
                swap_choice = self._wait_for_choice(player, available_creatures)
                
                if isinstance(swap_choice, Button):
                    continue  # Back button pressed
                else:
                    return ("swap", swap_choice.thing)

    def resolve_turn(self, player_action: ActionType, bot_action: ActionType):
        # Handle swaps first
        if player_action[0] == "swap":
            self.player.active_creature = player_action[1]
            self._show_text(self.player, f"You swapped to {player_action[1].display_name}!")
            
        if bot_action[0] == "swap":
            self.opponent.active_creature = bot_action[1]
            self._show_text(self.player, f"Foe swapped to {bot_action[1].display_name}!")

        # Then handle attacks
        if player_action[0] == "attack" and bot_action[0] == "attack":
            # Determine order based on speed
            if self.player.active_creature.speed > self.opponent.active_creature.speed:
                self.execute_attack(self.player, self.opponent, player_action[1])
                if self.opponent.active_creature.hp > 0:
                    self.execute_attack(self.opponent, self.player, bot_action[1])
            else:
                self.execute_attack(self.opponent, self.player, bot_action[1])
                if self.player.active_creature.hp > 0:
                    self.execute_attack(self.player, self.opponent, player_action[1])

    def execute_attack(self, attacker, defender, skill: Skill):
        # Calculate damage
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender.active_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender.active_creature.sp_defense) * skill.base_damage

        # Apply type effectiveness
        multiplier = self.get_type_multiplier(skill.skill_type, defender.active_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        
        defender.active_creature.hp = max(0, defender.active_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{attacker.active_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {defender.active_creature.display_name}!")

        if defender.active_creature.hp <= 0:
            self.handle_knockout(defender)

    def get_type_multiplier(self, skill_type: str, defender_type: str) -> float:
        if skill_type == defender_type or skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_knockout(self, player):
        self._show_text(self.player, f"{player.active_creature.display_name} was knocked out!")
        
        available_creatures = [c for c in player.creatures if c.hp > 0]
        if available_creatures:
            if player == self.player:
                swap_choice = self._wait_for_choice(player, [SelectThing(c) for c in available_creatures])
                player.active_creature = swap_choice.thing
            else:
                player.active_creature = available_creatures[0]
            self._show_text(self.player, f"{player.display_name} sent out {player.active_creature.display_name}!")

    def check_battle_end(self) -> bool:
        player_has_creatures = any(c.hp > 0 for c in self.player.creatures)
        opponent_has_creatures = any(c.hp > 0 for c in self.opponent.creatures)
        
        if not player_has_creatures:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif not opponent_has_creatures:
            self._show_text(self.player, "You won the battle!")
            return True
            
        return False
