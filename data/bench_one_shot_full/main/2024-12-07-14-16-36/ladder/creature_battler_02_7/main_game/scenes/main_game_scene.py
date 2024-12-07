from mini_game_engine.engine.lib import AbstractGameScene, Button
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
        return f"""=== Battle ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{', '.join(skill.display_name for skill in self.player_creature.skills)}
"""

    def run(self):
        self._show_text(self.player, "Battle Start!")
        
        while True:
            # Player choice phase
            self.player_chosen_skill = self._get_skill_choice(self.player, self.player_creature)
            
            # Opponent choice phase
            self.opponent_chosen_skill = self._get_skill_choice(self.opponent, self.opponent_creature)
            
            # Resolution phase
            self._resolve_turn()
            
            # Check for battle end
            if self.player_creature.hp <= 0:
                self._show_text(self.player, "You lost!")
                break
            elif self.opponent_creature.hp <= 0:
                self._show_text(self.player, "You won!")
                break

        self._transition_to_scene("MainMenuScene")

    def _get_skill_choice(self, player, creature):
        choices = [Button(skill.display_name) for skill in creature.skills]
        choice = self._wait_for_choice(player, choices)
        return creature.skills[choices.index(choice)]

    def _resolve_turn(self):
        # Determine order based on speed
        if self.player_creature.speed > self.opponent_creature.speed:
            first, second = self.player, self.opponent
            first_skill, second_skill = self.player_chosen_skill, self.opponent_chosen_skill
        elif self.opponent_creature.speed > self.player_creature.speed:
            first, second = self.opponent, self.player
            first_skill, second_skill = self.opponent_chosen_skill, self.player_chosen_skill
        else:
            if random.random() < 0.5:
                first, second = self.player, self.opponent
                first_skill, second_skill = self.player_chosen_skill, self.opponent_chosen_skill
            else:
                first, second = self.opponent, self.player
                first_skill, second_skill = self.opponent_chosen_skill, self.player_chosen_skill

        # Execute skills
        self._execute_skill(first, first_skill)
        if self.player_creature.hp > 0 and self.opponent_creature.hp > 0:
            self._execute_skill(second, second_skill)

    def _execute_skill(self, attacker, skill):
        if attacker == self.player:
            atk_creature = self.player_creature
            def_creature = self.opponent_creature
        else:
            atk_creature = self.opponent_creature
            def_creature = self.player_creature

        damage = atk_creature.attack + skill.base_damage - def_creature.defense
        def_creature.hp = max(0, def_creature.hp - damage)
        
        self._show_text(self.player, 
            f"{atk_creature.display_name} used {skill.display_name}! "
            f"Dealt {damage} damage to {def_creature.display_name}!")
