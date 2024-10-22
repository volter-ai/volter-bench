from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.foe = app.create_bot("basic_opponent")
        self.player.active_creature = self.player.creatures[0]
        self.foe.active_creature = self.foe.creatures[0]

    def __str__(self):
        player_creature = self.player.active_creature
        foe_creature = self.foe.active_creature
        return f"""===Battle===
Your {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
Foe's {foe_creature.display_name}: HP {foe_creature.hp}/{foe_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._show_text(self.player, "Battle start!")
        self.game_loop()

    def game_loop(self):
        while True:
            player_action = self.player_choice_phase()
            foe_action = self.foe_choice_phase()
            
            actions = [player_action, foe_action]
            actions.sort(key=lambda x: (x[0] != "swap", -x[1].active_creature.speed))
            
            for action_type, actor, target in actions:
                if action_type == "swap":
                    self.perform_swap(actor, target)
                elif action_type == "skill":
                    self.perform_skill(actor, target)
            
            if self.check_battle_end():
                break
        
        self._transition_to_scene("MainMenuScene")

    def player_choice_phase(self):
        return self.choose_action(self.player)

    def foe_choice_phase(self):
        return self.choose_action(self.foe)

    def choose_action(self, current_player):
        attack_button = Button("Attack")
        choices = [attack_button]
        
        if self.get_available_creatures(current_player):
            swap_button = Button("Swap")
            choices.append(swap_button)
        
        choice = self._wait_for_choice(current_player, choices)

        if choice.display_name == "Attack":
            return self.choose_skill(current_player)
        elif choice.display_name == "Swap":
            return self.choose_swap(current_player)

    def choose_skill(self, current_player):
        skill_choices = [SelectThing(skill) for skill in current_player.active_creature.skills]
        back_button = Button("Back")
        skill_choices.append(back_button)
        
        skill_choice = self._wait_for_choice(current_player, skill_choices)
        
        if skill_choice == back_button:
            return self.choose_action(current_player)
        else:
            return ("skill", current_player, skill_choice.thing)

    def choose_swap(self, current_player):
        available_creatures = self.get_available_creatures(current_player)
        if not available_creatures:
            return self.choose_skill(current_player)  # If no creatures to swap, force attack
        
        creature_choices = [SelectThing(creature) for creature in available_creatures]
        back_button = Button("Back")
        creature_choices.append(back_button)
        
        creature_choice = self._wait_for_choice(current_player, creature_choices)
        
        if creature_choice == back_button:
            return self.choose_action(current_player)
        else:
            return ("swap", current_player, creature_choice.thing)

    def get_available_creatures(self, player):
        return [creature for creature in player.creatures if creature.hp > 0 and creature != player.active_creature]

    def perform_swap(self, actor, new_creature):
        actor.active_creature = new_creature
        self._show_text(self.player, f"{actor.display_name} swapped to {new_creature.display_name}!")

    def perform_skill(self, actor, skill):
        defender = self.foe if actor == self.player else self.player
        damage = self.calculate_damage(actor.active_creature, defender.active_creature, skill)
        defender.active_creature.hp = max(0, defender.active_creature.hp - damage)
        self._show_text(self.player, f"{actor.active_creature.display_name} used {skill.display_name} and dealt {damage} damage!")

        if defender.active_creature.hp == 0:
            self._show_text(self.player, f"{defender.active_creature.display_name} was knocked out!")
            self.force_swap(defender)

    def calculate_damage(self, attacker, defender, skill):
        if skill.is_physical:
            raw_damage = attacker.attack + skill.base_damage - defender.defense
        else:
            raw_damage = (attacker.sp_attack / defender.sp_defense) * skill.base_damage

        type_factor = self.get_type_factor(skill.skill_type, defender.creature_type)
        final_damage = int(type_factor * raw_damage)
        return max(1, final_damage)

    def get_type_factor(self, skill_type, defender_type):
        effectiveness = {
            "fire": {"leaf": 2, "water": 0.5},
            "water": {"fire": 2, "leaf": 0.5},
            "leaf": {"water": 2, "fire": 0.5}
        }
        return effectiveness.get(skill_type, {}).get(defender_type, 1)

    def force_swap(self, player):
        available_creatures = self.get_available_creatures(player)
        if not available_creatures:
            return

        if len(available_creatures) == 1:
            new_creature = available_creatures[0]
        else:
            creature_choices = [SelectThing(creature) for creature in available_creatures]
            new_creature = self._wait_for_choice(player, creature_choices).thing

        player.active_creature = new_creature
        self._show_text(self.player, f"{player.display_name} sent out {new_creature.display_name}!")

    def check_battle_end(self):
        if all(creature.hp == 0 for creature in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(creature.hp == 0 for creature in self.foe.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False
