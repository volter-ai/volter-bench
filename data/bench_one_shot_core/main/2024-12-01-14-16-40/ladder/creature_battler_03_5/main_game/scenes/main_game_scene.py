from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_chosen_skill = None
        self.opponent_chosen_skill = None

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, f"Battle Start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            # Player Choice Phase
            self.player_chosen_skill = self._handle_player_turn(self.player, self.player_creature)
            
            # Opponent Choice Phase
            self.opponent_chosen_skill = self._handle_player_turn(self.opponent, self.opponent_creature)
            
            # Resolution Phase
            self._resolve_turn()
            
            # Check for battle end
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break
        
        self._transition_to_scene("MainMenuScene")

    def _handle_player_turn(self, player, creature):
        choices = [SelectThing(skill) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return choice.thing

    def _calculate_damage(self, attacker_skill, attacker, defender):
        # Calculate raw damage
        raw_damage = attacker.attack + attacker_skill.base_damage - defender.defense
        
        # Calculate type multiplier
        multiplier = self._get_type_multiplier(attacker_skill.skill_type, defender.creature_type)
        
        # Calculate final damage
        return int(raw_damage * multiplier)

    def _get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def _resolve_turn(self):
        # Determine order based on speed
        if self.player_creature.speed > self.opponent_creature.speed:
            first = (self.player, self.player_creature, self.player_chosen_skill)
            second = (self.opponent, self.opponent_creature, self.opponent_chosen_skill)
        elif self.opponent_creature.speed > self.player_creature.speed:
            first = (self.opponent, self.opponent_creature, self.opponent_chosen_skill)
            second = (self.player, self.player_creature, self.player_chosen_skill)
        else:
            # Random order if speeds are equal
            options = [(self.player, self.player_creature, self.player_chosen_skill),
                      (self.opponent, self.opponent_creature, self.opponent_chosen_skill)]
            random.shuffle(options)
            first, second = options

        # Execute moves in order
        self._execute_move(*first, second[1])
        if second[1].hp > 0:  # Only execute second move if target still alive
            self._execute_move(*second, first[1])

    def _execute_move(self, attacker, attacker_creature, skill, defender_creature):
        damage = self._calculate_damage(skill, attacker_creature, defender_creature)
        defender_creature.hp = max(0, defender_creature.hp - damage)
        self._show_text(self.player, 
            f"{attacker_creature.display_name} used {skill.display_name}! "
            f"Dealt {damage} damage to {defender_creature.display_name}")
