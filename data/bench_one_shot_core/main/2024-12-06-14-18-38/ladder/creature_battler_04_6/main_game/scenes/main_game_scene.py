from mini_game_engine.engine.lib import AbstractGameScene, SelectThing
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
        
        return f"""=== Battle ===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.opponent.display_name}'s {opponent_creature.display_name}: HP {opponent_creature.hp}/{opponent_creature.max_hp}

Phase: {self.phase}

Available Skills:
{self._format_skills(player_creature.skills)}
"""

    def _format_skills(self, skills):
        return "\n".join([f"> {skill.display_name} ({skill.skill_type} type, {'Physical' if skill.is_physical else 'Special'})" for skill in skills])

    def _calculate_damage(self, attacker_creature, defender_creature, skill):
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
            # Player choice phase
            self.phase = "player_choice"
            player_creature = self.player.creatures[0]
            choice = self._wait_for_choice(
                self.player,
                [SelectThing(skill, label=skill.display_name) for skill in player_creature.skills]
            )
            self.player_skill = choice.thing

            # Opponent choice phase
            self.phase = "opponent_choice"
            opponent_creature = self.opponent.creatures[0]
            choice = self._wait_for_choice(
                self.opponent,
                [SelectThing(skill, label=skill.display_name) for skill in opponent_creature.skills]
            )
            self.opponent_skill = choice.thing

            # Resolution phase
            self.phase = "resolution"
            
            # Determine order
            first = self.player
            second = self.opponent
            if opponent_creature.speed > player_creature.speed or \
               (opponent_creature.speed == player_creature.speed and random.random() < 0.5):
                first, second = second, first

            # Execute skills
            for attacker, defender, skill in [(first, second, self.player_skill), (second, first, self.opponent_skill)]:
                attacker_creature = attacker.creatures[0]
                defender_creature = defender.creatures[0]
                
                damage = self._calculate_damage(attacker_creature, defender_creature, skill)
                defender_creature.hp = max(0, defender_creature.hp - damage)
                
                self._show_text(self.player, f"{attacker_creature.display_name} used {skill.display_name}!")
                self._show_text(self.player, f"It dealt {damage} damage!")

                if defender_creature.hp <= 0:
                    winner = attacker.display_name
                    self._show_text(self.player, f"{winner} wins!")
                    self._transition_to_scene("MainMenuScene")
                    return
