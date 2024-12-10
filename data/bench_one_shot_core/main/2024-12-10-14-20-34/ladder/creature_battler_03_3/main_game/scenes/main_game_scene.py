from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        while True:
            # Player Choice Phase
            player_skill = self._handle_player_turn()
            
            # Opponent Choice Phase  
            opponent_skill = self._handle_opponent_turn()

            # Resolution Phase
            self._resolve_turn(player_skill, opponent_skill)

            # Check for battle end
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost the battle!")
                self._quit_whole_game()
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won the battle!")
                play_again = Button("Play Again")
                quit_button = Button("Quit")
                choice = self._wait_for_choice(self.player, [play_again, quit_button])
                
                if choice == play_again:
                    self._transition_to_scene("MainMenuScene")
                else:
                    self._quit_whole_game()

    def _handle_player_turn(self):
        self._show_text(self.player, "Choose your skill!")
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        return self._wait_for_choice(self.player, choices).thing

    def _handle_opponent_turn(self):
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        return self._wait_for_choice(self.opponent, choices).thing

    def _calculate_damage(self, skill, attacker, defender):
        raw_damage = attacker.attack + skill.base_damage - defender.defense
        
        # Type effectiveness
        multiplier = self._get_type_multiplier(skill.skill_type, defender.creature_type)
        
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

    def _resolve_turn(self, player_skill, opponent_skill):
        # Determine order based on speed
        if self.player_creature.speed > self.opponent_creature.speed:
            first = (self.player, self.player_creature, player_skill, self.opponent_creature)
            second = (self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
        elif self.player_creature.speed < self.opponent_creature.speed:
            first = (self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
            second = (self.player, self.player_creature, player_skill, self.opponent_creature)
        else:
            if random.random() < 0.5:
                first = (self.player, self.player_creature, player_skill, self.opponent_creature)
                second = (self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
            else:
                first = (self.opponent, self.opponent_creature, opponent_skill, self.player_creature)
                second = (self.player, self.player_creature, player_skill, self.opponent_creature)

        # Execute moves in order
        for actor, attacker, skill, defender in [first, second]:
            if defender.hp > 0:  # Only attack if defender still alive
                damage = self._calculate_damage(skill, attacker, defender)
                defender.hp = max(0, defender.hp - damage)
                self._show_text(actor, f"{attacker.display_name} used {skill.display_name}! Dealt {damage} damage!")
