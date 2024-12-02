from mini_game_engine.engine.lib import AbstractGameScene, Button
from main_game.models import Player, Creature, Skill

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.phase = "player_choice"
        self.queued_skills = {}  # Will store {player_uid: skill}
        
        # Type effectiveness matrix
        self.type_effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5},
            "normal": {}
        }

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Phase: {self.phase}
"""

    def run(self):
        self._show_text(self.player, f"Battle start! {self.player_creature.display_name} vs {self.opponent_creature.display_name}")
        
        while True:
            if self.phase == "player_choice":
                self.handle_player_choice()
            elif self.phase == "opponent_choice":
                self.handle_opponent_choice()
            elif self.phase == "resolution":
                self.resolve_turn()

            if self.check_battle_end():
                self._quit_whole_game()  # Properly end the game when battle is over

    def handle_player_choice(self):
        choices = [Button(skill.display_name) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        selected_skill = next(skill for skill in self.player_creature.skills 
                            if skill.display_name == choice.display_name)
        self.queued_skills[self.player.uid] = selected_skill
        self.phase = "opponent_choice"

    def handle_opponent_choice(self):
        choices = [Button(skill.display_name) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        selected_skill = next(skill for skill in self.opponent_creature.skills 
                            if skill.display_name == choice.display_name)
        self.queued_skills[self.opponent.uid] = selected_skill
        self.phase = "resolution"

    def calculate_damage(self, attacker_creature: Creature, defender_creature: Creature, skill: Skill) -> int:
        raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        
        # Get type effectiveness
        effectiveness = self.type_effectiveness.get(skill.skill_type, {}).get(defender_creature.creature_type, 1.0)
        
        final_damage = int(raw_damage * effectiveness)
        return max(0, final_damage)

    def resolve_turn(self):
        # Determine order
        first = self.player if self.player_creature.speed > self.opponent_creature.speed else self.opponent
        if self.player_creature.speed == self.opponent_creature.speed:
            import random
            first = random.choice([self.player, self.opponent])
        second = self.opponent if first == self.player else self.player

        # Execute moves in order
        for current in [first, second]:
            attacker = self.player_creature if current == self.player else self.opponent_creature
            defender = self.opponent_creature if current == self.player else self.player_creature
            skill = self.queued_skills[current.uid]

            damage = self.calculate_damage(attacker, defender, skill)
            defender.hp -= damage
            
            self._show_text(self.player, 
                f"{attacker.display_name} used {skill.display_name}! Dealt {damage} damage!")

        self.queued_skills.clear()
        self.phase = "player_choice"

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False
