import random

from mini_game_engine.engine.lib import AbstractGameScene, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.reset_creatures()

    def reset_creatures(self):
        self.player_creature = self.player.creatures[0]
        self.opponent_creature = self.opponent.creatures[0]
        self.player_creature.hp = self.player_creature.max_hp
        self.opponent_creature.hp = self.opponent_creature.max_hp

    def __str__(self):
        return f"""===Battle===
{self.player.display_name}'s {self.player_creature.display_name}: HP {self.player_creature.hp}/{self.player_creature.max_hp}
{self.opponent.display_name}'s {self.opponent_creature.display_name}: HP {self.opponent_creature.hp}/{self.opponent_creature.max_hp}

Available skills:
{', '.join([skill.display_name for skill in self.player_creature.skills])}
"""

    def run(self):
        self.reset_creatures()
        self._show_text(self.player, f"A wild {self.opponent_creature.display_name} appears!")
        
        while True:
            # Player Choice Phase
            player_skill = self.player_choice_phase()
            
            # Foe Choice Phase
            foe_skill = self.foe_choice_phase()
            
            # Resolution Phase
            self.resolution_phase(player_skill, foe_skill)
            
            if self.check_battle_end():
                break

        self._show_text(self.player, "Returning to Main Menu...")
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        self._show_text(self.player, f"Available skills for {self.player_creature.display_name}:")
        for skill in self.player_creature.skills:
            self._show_text(self.player, f"- {skill.display_name}")
        
        choices = [SelectThing(skill) for skill in self.player_creature.skills]
        choice = self._wait_for_choice(self.player, choices)
        return choice.thing

    def foe_choice_phase(self):
        self._show_text(self.opponent, f"Available skills for {self.opponent_creature.display_name}:")
        for skill in self.opponent_creature.skills:
            self._show_text(self.opponent, f"- {skill.display_name}")
        
        choices = [SelectThing(skill) for skill in self.opponent_creature.skills]
        choice = self._wait_for_choice(self.opponent, choices)
        return choice.thing

    def resolution_phase(self, player_skill, foe_skill):
        first, second = self.determine_order(self.player_creature, self.opponent_creature)
        
        self.execute_skill(first[0], first[1], second[0], second[1], player_skill if first[0] == self.player else foe_skill)
        if not self.check_battle_end():
            self.execute_skill(second[0], second[1], first[0], first[1], foe_skill if second[0] == self.opponent else player_skill)

    def determine_order(self, creature1, creature2):
        if creature1.speed > creature2.speed:
            return (self.player, creature1), (self.opponent, creature2)
        elif creature2.speed > creature1.speed:
            return (self.opponent, creature2), (self.player, creature1)
        else:
            if random.choice([True, False]):
                return (self.player, creature1), (self.opponent, creature2)
            else:
                return (self.opponent, creature2), (self.player, creature1)

    def execute_skill(self, attacker, attacker_creature, defender, defender_creature, skill):
        damage = attacker_creature.attack + skill.base_damage - defender_creature.defense
        damage = max(0, damage)  # Ensure damage is not negative
        
        defender_creature.hp -= damage
        defender_creature.hp = max(0, defender_creature.hp)  # Ensure HP doesn't go below 0
        
        self._show_text(self.player, f"{attacker.display_name}'s {attacker_creature.display_name} uses {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender_creature.display_name} takes {damage} damage!")

    def check_battle_end(self):
        if self.player_creature.hp <= 0:
            self._show_text(self.player, f"{self.player.display_name}'s {self.player_creature.display_name} fainted!")
            self._show_text(self.player, "You lose the battle!")
            return True
        elif self.opponent_creature.hp <= 0:
            self._show_text(self.player, f"{self.opponent.display_name}'s {self.opponent_creature.display_name} fainted!")
            self._show_text(self.player, "You win the battle!")
            return True
        return False
