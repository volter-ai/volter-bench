from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.player_creature = player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}: {self.player_creature.display_name} (HP: {self.player_creature.hp}/{self.player_creature.max_hp})
{self.opponent.display_name}: {self.opponent_creature.display_name} (HP: {self.opponent_creature.hp}/{self.opponent_creature.max_hp})

Player's turn:
> Use Skill
"""

    def run(self):
        while True:
            self._show_text(self.player, str(self))
            
            # Player turn
            player_skill = self.player_turn()
            
            # Opponent turn
            opponent_skill = self.opponent_turn()
            
            # Resolve turn
            self.resolve_turn(player_skill, opponent_skill)
            
            # Check for battle end
            if self.check_battle_end():
                break
        
        self.reset_creatures()
        self._transition_to_scene("MainMenuScene")

    def player_turn(self):
        use_skill_button = Button("Use Skill")
        choice = self._wait_for_choice(self.player, [use_skill_button])
        
        if use_skill_button == choice:
            skill_choices = [SelectThing(skill) for skill in self.player_creature.skills]
            skill_choice = self._wait_for_choice(self.player, skill_choices)
            return skill_choice.thing

    def opponent_turn(self):
        skill_choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        skill_choice = self._wait_for_choice(self.opponent, skill_choices)
        return skill_choice.thing

    def resolve_turn(self, player_skill, opponent_skill):
        if self.player_creature.speed > self.opponent_creature.speed:
            first, second = (self.player, self.player_creature, player_skill), (self.opponent, self.opponent_creature, opponent_skill)
        elif self.player_creature.speed < self.opponent_creature.speed:
            first, second = (self.opponent, self.opponent_creature, opponent_skill), (self.player, self.player_creature, player_skill)
        else:
            # If speeds are equal, randomly choose who goes first
            if random.choice([True, False]):
                first, second = (self.player, self.player_creature, player_skill), (self.opponent, self.opponent_creature, opponent_skill)
            else:
                first, second = (self.opponent, self.opponent_creature, opponent_skill), (self.player, self.player_creature, player_skill)

        self.execute_skill(*first, second[1])
        if second[1].hp > 0:
            self.execute_skill(*second, first[1])

    def execute_skill(self, attacker, attacker_creature, skill, defender_creature):
        if skill.is_physical:
            raw_damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage
        
        weakness_factor = self.calculate_weakness_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(weakness_factor * raw_damage)
        
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        
        self._show_text(attacker, f"{attacker_creature.display_name} used {skill.display_name}!")
        self._show_text(attacker, f"{defender_creature.display_name} took {final_damage} damage!")

    def calculate_weakness_factor(self, skill_type, creature_type):
        if skill_type.lower() == "normal":
            return 1  # Normal type is neither effective nor ineffective against any type
        
        weakness_chart = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return weakness_chart.get(skill_type.lower(), {}).get(creature_type.lower(), 1)

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, "You lost the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, "You won the battle!")
            return True
        return False

    def reset_creatures(self):
        for creature in self.player.creatures + self.opponent.creatures:
            creature.hp = creature.max_hp
