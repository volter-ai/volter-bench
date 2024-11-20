from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.phase = "player_choice"
        self.player_skill = None
        self.opponent_skill = None
        
        # Reset creatures to full HP
        for creature in self.player.creatures:
            creature.hp = creature.max_hp
        for creature in self.opponent.creatures:
            creature.hp = creature.max_hp

    def __str__(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]
        
        return f"""=== Battle Scene ===
Your {player_creature.display_name}: {player_creature.hp}/{player_creature.max_hp} HP
Opponent's {opponent_creature.display_name}: {opponent_creature.hp}/{opponent_creature.max_hp} HP

Phase: {self.phase}

Available Skills:
{self._format_skills(player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name}" for skill in skills])

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Calculate type multiplier
        multiplier = 1.0
        if skill.skill_type == "fire":
            if defender_creature.creature_type == "leaf":
                multiplier = 2.0
            elif defender_creature.creature_type == "water":
                multiplier = 0.5
        elif skill.skill_type == "water":
            if defender_creature.creature_type == "fire":
                multiplier = 2.0
            elif defender_creature.creature_type == "leaf":
                multiplier = 0.5
        elif skill.skill_type == "leaf":
            if defender_creature.creature_type == "water":
                multiplier = 2.0
            elif defender_creature.creature_type == "fire":
                multiplier = 0.5

        return int(raw_damage * multiplier)

    def run(self):
        while True:
            if self.phase == "player_choice":
                choices = [Button(skill.display_name) for skill in self.player.creatures[0].skills]
                choice = self._wait_for_choice(self.player, choices)
                self.player_skill = next(s for s in self.player.creatures[0].skills 
                                      if s.display_name == choice.display_name)
                self.phase = "opponent_choice"
                
            elif self.phase == "opponent_choice":
                choices = [Button(skill.display_name) for skill in self.opponent.creatures[0].skills]
                choice = self._wait_for_choice(self.opponent, choices)
                self.opponent_skill = next(s for s in self.opponent.creatures[0].skills 
                                        if s.display_name == choice.display_name)
                self.phase = "resolution"
                
            else:  # resolution phase
                player_creature = self.player.creatures[0]
                opponent_creature = self.opponent.creatures[0]
                
                # Determine order
                first = player_creature if player_creature.speed > opponent_creature.speed else opponent_creature
                second = opponent_creature if first == player_creature else player_creature
                if player_creature.speed == opponent_creature.speed:
                    first, second = random.choice([(player_creature, opponent_creature), 
                                                 (opponent_creature, player_creature)])

                # Execute moves
                for attacker, defender, skill in [(first, second, self.player_skill if first == player_creature else self.opponent_skill),
                                                (second, first, self.opponent_skill if first == player_creature else self.player_skill)]:
                    if defender.hp > 0:  # Only attack if defender still alive
                        damage = self.calculate_damage(attacker, defender, skill)
                        defender.hp = max(0, defender.hp - damage)
                        self._show_text(self.player, 
                                      f"{attacker.display_name} used {skill.display_name} for {damage} damage!")
                        
                        if defender.hp == 0:
                            winner = "You" if defender == opponent_creature else "Opponent"
                            self._show_text(self.player, f"{winner} won the battle!")
                            self._transition_to_scene("MainMenuScene")
                            return

                self.phase = "player_choice"
