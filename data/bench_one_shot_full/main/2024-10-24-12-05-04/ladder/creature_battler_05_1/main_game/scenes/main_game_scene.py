from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.opponent = app.create_bot("basic_opponent")
        self.turn_queue = []
        self.battle_ended = False

    def __str__(self):
        player_creature = self.player.active_creature
        opponent_creature = self.opponent.active_creature
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.opponent.display_name}'s {opponent_creature.display_name}: HP {opponent_creature.hp}/{opponent_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._show_text(self.player, "Battle start!")
        self._show_text(self.opponent, "Battle start!")
        
        while not self.battle_ended:
            self.player_choice_phase()
            self.foe_choice_phase()
            self.resolution_phase()
            
            if self.check_battle_end():
                self.battle_ended = True
        
        self.reset_creatures()
        self._quit_whole_game()

    def player_choice_phase(self):
        self.get_player_action(self.player)

    def foe_choice_phase(self):
        self.get_player_action(self.opponent)

    def get_player_action(self, player):
        choices = []
        
        if player.active_creature.skills:
            choices.append(Button("Attack"))
        
        available_creatures = [creature for creature in player.creatures if creature.hp > 0 and creature != player.active_creature]
        if available_creatures:
            choices.append(Button("Swap"))
        
        if not choices:
            self._show_text(player, f"{player.active_creature.display_name} has no available actions!")
            return
        
        choice = self._wait_for_choice(player, choices)

        if choice.display_name == "Attack":
            skill_choices = [SelectThing(skill) for skill in player.active_creature.skills]
            skill_choice = self._wait_for_choice(player, skill_choices)
            self.turn_queue.append(("attack", player, skill_choice.thing))
        elif choice.display_name == "Swap":
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            creature_choice = self._wait_for_choice(player, creature_choices)
            self.turn_queue.append(("swap", player, creature_choice.thing))

    def resolution_phase(self):
        self.turn_queue.sort(key=lambda x: x[1].active_creature.speed if x[0] == "attack" else float('inf'), reverse=True)

        for action, player, target in self.turn_queue:
            if action == "swap":
                player.active_creature = target
                self._show_text(self.player, f"{player.display_name} swapped to {target.display_name}!")
                self._show_text(self.opponent, f"{player.display_name} swapped to {target.display_name}!")
            elif action == "attack":
                self.execute_attack(player, target)

        self.turn_queue.clear()

    def execute_attack(self, attacker, skill):
        defender = self.player if attacker == self.opponent else self.opponent
        damage = self.calculate_damage(attacker.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)

        self._show_text(self.player, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.opponent, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} took {damage} damage!")
        self._show_text(self.opponent, f"{defender.display_name}'s {defender.active_creature.display_name} took {damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
            self._show_text(self.opponent, f"{defender.display_name}'s {defender.active_creature.display_name} fainted!")
            self.force_swap(defender)

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_effectiveness = self.get_type_effectiveness(skill.skill_type, defender.creature_type)
        final_damage = int(raw_damage * type_effectiveness)
        return max(1, final_damage)  # Ensure at least 1 damage is dealt

    def get_type_effectiveness(self, skill_type, defender_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, defender_type), 1)

    def force_swap(self, player):
        available_creatures = [creature for creature in player.creatures if creature.hp > 0]
        if not available_creatures:
            return

        if len(available_creatures) == 1:
            player.active_creature = available_creatures[0]
        else:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            creature_choice = self._wait_for_choice(player, creature_choices)
            player.active_creature = creature_choice.thing

        self._show_text(self.player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        self._show_text(self.opponent, f"{player.display_name} sent out {player.active_creature.display_name}!")

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            self._show_text(self.opponent, "You won the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.opponent.creatures):
            self._show_text(self.player, "You won the battle!")
            self._show_text(self.opponent, "You lost the battle!")
            return True
        return False

    def reset_creatures(self):
        for player in [self.player, self.opponent]:
            for creature in player.creatures:
                creature.hp = creature.max_hp
