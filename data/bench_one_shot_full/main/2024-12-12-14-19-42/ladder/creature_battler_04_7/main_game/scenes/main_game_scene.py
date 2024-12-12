from mini_game_engine.engine.lib import AbstractGameScene, Button
import random

class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.phase = "player_choice"
        self.player_skill = None
        self.opponent_skill = None
        
    def __str__(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]
        
        return f"""=== Battle ===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.opponent.display_name}'s {opponent_creature.display_name}: HP {opponent_creature.hp}/{opponent_creature.max_hp}

Phase: {self.phase}
Available Skills: {[skill.display_name for skill in player_creature.skills]}"""

    def run(self):
        while True:
            if self.phase == "player_choice":
                self.handle_player_choice()
            elif self.phase == "opponent_choice":
                self.handle_opponent_choice()
            else:  # resolution phase
                self.handle_resolution()
                
            if self.check_battle_end():
                break

        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def handle_player_choice(self):
        player_creature = self.player.creatures[0]
        choices = [Button(skill.display_name) for skill in player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        self.player_skill = next(s for s in player_creature.skills if s.display_name == choice.display_name)
        self.phase = "opponent_choice"

    def handle_opponent_choice(self):
        opponent_creature = self.opponent.creatures[0]
        choices = [Button(skill.display_name) for skill in opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        self.opponent_skill = next(s for s in opponent_creature.skills if s.display_name == choice.display_name)
        self.phase = "resolution"

    def calculate_damage(self, attacker_creature, defender_creature, skill):
        # Calculate raw damage
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage

        # Calculate type multiplier
        multiplier = self.get_type_multiplier(skill.skill_type, defender_creature.creature_type)
        
        return int(raw_damage * multiplier)

    def get_type_multiplier(self, skill_type, defender_type):
        if skill_type == "normal":
            return 1.0
            
        effectiveness = {
            "fire": {"leaf": 2.0, "water": 0.5},
            "water": {"fire": 2.0, "leaf": 0.5},
            "leaf": {"water": 2.0, "fire": 0.5}
        }
        
        return effectiveness.get(skill_type, {}).get(defender_type, 1.0)

    def handle_resolution(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        # Determine order
        first = (player_creature, self.player_skill) if player_creature.speed > opponent_creature.speed or \
               (player_creature.speed == opponent_creature.speed and random.random() < 0.5) else \
               (opponent_creature, self.opponent_skill)
        second = (opponent_creature, self.opponent_skill) if first[0] == player_creature else \
                (player_creature, self.player_skill)

        # Execute moves in order
        for attacker, skill in [first, second]:
            defender = opponent_creature if attacker == player_creature else player_creature
            damage = self.calculate_damage(attacker, defender, skill)
            defender.hp = max(0, defender.hp - damage)
            
            self._show_text(self.player, f"{attacker.display_name} used {skill.display_name} for {damage} damage!")
            
            if defender.hp == 0:
                break

        self.phase = "player_choice"
        self.player_skill = None
        self.opponent_skill = None

    def check_battle_end(self):
        player_creature = self.player.creatures[0]
        opponent_creature = self.opponent.creatures[0]

        if player_creature.hp == 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif opponent_creature.hp == 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
