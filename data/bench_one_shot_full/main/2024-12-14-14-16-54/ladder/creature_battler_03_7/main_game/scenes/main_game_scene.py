from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.queued_skills = {}  # Will use player.uid as key instead of player object

    def __str__(self):
        return f"""=== Battle Scene ===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available Skills:
{chr(10).join([f"> {skill.display_name} ({skill.skill_type} - {skill.base_damage} damage)" for skill in self.player_creature.skills])}
"""

    def run(self):
        while True:
            # Player Choice Phase
            self._show_text(self.player, "Your turn! Choose a skill:")
            player_skill = self._wait_for_choice(self.player, 
                [Button(skill.display_name) for skill in self.player_creature.skills]).display_name
            self.queued_skills[self.player.uid] = next(s for s in self.player_creature.skills if s.display_name == player_skill)

            # Opponent Choice Phase
            self._show_text(self.opponent, "Enemy turn!")
            opponent_skill = self._wait_for_choice(self.opponent,
                [Button(skill.display_name) for skill in self.opponent_creature.skills]).display_name
            self.queued_skills[self.opponent.uid] = next(s for s in self.opponent_creature.skills if s.display_name == opponent_skill)

            # Resolution Phase
            first, second = self.determine_order()
            self.resolve_skill(first)
            if self.check_battle_end():
                break
            self.resolve_skill(second)
            if self.check_battle_end():
                break

            self.queued_skills.clear()

    def determine_order(self):
        if self.player_creature.speed > self.opponent_creature.speed:
            return self.player, self.opponent
        elif self.player_creature.speed < self.opponent_creature.speed:
            return self.opponent, self.player
        else:
            return random.sample([self.player, self.opponent], 2)

    def get_type_multiplier(self, skill_type: str, creature_type: str) -> float:
        if skill_type == creature_type:
            return 1.0
        
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(creature_type, 1.0)

    def resolve_skill(self, attacker):
        skill = self.queued_skills[attacker.uid]
        if attacker == self.player:
            atk_creature = self.player_creature
            def_creature = self.opponent_creature
        else:
            atk_creature = self.opponent_creature
            def_creature = self.player_creature

        raw_damage = atk_creature.attack + skill.base_damage - def_creature.defense
        multiplier = self.get_type_multiplier(skill.skill_type, def_creature.creature_type)
        final_damage = int(raw_damage * multiplier)
        final_damage = max(1, final_damage)  # Minimum 1 damage

        def_creature.hp = max(0, def_creature.hp - final_damage)
        
        self._show_text(self.player, 
            f"{atk_creature.display_name} used {skill.display_name}! "
            f"Dealt {final_damage} damage to {def_creature.display_name}!")

    def check_battle_end(self) -> bool:
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"Your {self.player_creature.display_name} was defeated! You lose!")
            self._transition_to_scene("MainMenuScene")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"Enemy {self.opponent_creature.display_name} was defeated! You win!")
            self._transition_to_scene("MainMenuScene")
            return True
        return False
