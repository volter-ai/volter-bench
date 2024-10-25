from mini_game_engine.engine.lib import AbstractGameScene, Button, SelectThing
import random


class MainGameScene(AbstractGameScene):
    def __init__(self, app, player):
        super().__init__(app, player)
        self.bot = self._app.create_bot("basic_opponent")

    def __str__(self):
        player_creature = self.player.active_creature
        bot_creature = self.bot.active_creature
        return f"""===Battle===
{self.player.display_name}'s {player_creature.display_name}: HP {player_creature.hp}/{player_creature.max_hp}
{self.bot.display_name}'s {bot_creature.display_name}: HP {bot_creature.hp}/{bot_creature.max_hp}

> Attack
> Swap
"""

    def run(self):
        self._initialize_battle()
        turn_queue = []
        while True:
            self._player_choice_phase(self.player, turn_queue)
            self._player_choice_phase(self.bot, turn_queue)
            self._resolution_phase(turn_queue)
            if self._check_battle_end():
                break
            turn_queue.clear()
        self._transition_to_scene("MainMenuScene")

    def _initialize_battle(self):
        self.player.active_creature = self.player.creatures[0]
        self.bot.active_creature = self.bot.creatures[0]

    def _player_choice_phase(self, player, turn_queue):
        while True:
            attack_button = Button("Attack")
            swap_button = Button("Swap")
            choices = [attack_button, swap_button]
            choice = self._wait_for_choice(player, choices)

            if choice == attack_button:
                skill = self._choose_skill(player)
                if skill:
                    turn_queue.append((player, "attack", skill))
                    break
            elif choice == swap_button:
                new_creature = self._choose_swap_creature(player)
                if new_creature:
                    turn_queue.append((player, "swap", new_creature))
                    break

    def _choose_skill(self, player):
        skills = player.active_creature.skills
        choices = [SelectThing(skill) for skill in skills] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _choose_swap_creature(self, player):
        available_creatures = [c for c in player.creatures if c != player.active_creature and c.hp > 0]
        choices = [SelectThing(creature) for creature in available_creatures] + [Button("Back")]
        choice = self._wait_for_choice(player, choices)
        return choice.thing if isinstance(choice, SelectThing) else None

    def _resolution_phase(self, turn_queue):
        turn_queue.sort(key=lambda x: (x[1] != "swap", -x[0].active_creature.speed, random.random()))
        
        for i, (player, action_type, action) in enumerate(turn_queue):
            if action_type == "swap":
                old_creature = player.active_creature
                player.active_creature = action
                self._show_text(player, f"{player.display_name} swapped {old_creature.display_name} for {action.display_name}!")
                
                # Execute opponent's queued skill on the swapped-in creature
                opponent = self.bot if player == self.player else self.player
                opponent_action = next((act for act in turn_queue[i+1:] if act[0] == opponent and act[1] == "attack"), None)
                if opponent_action:
                    self._execute_skill(opponent, opponent_action[2], player.active_creature)
            elif action_type == "attack":
                defender = self.bot if player == self.player else self.player
                self._execute_skill(player, action, defender.active_creature)

    def _execute_skill(self, attacker, skill, defender_creature):
        if skill.is_physical:
            raw_damage = attacker.active_creature.attack + skill.base_damage - defender_creature.defense
        else:
            raw_damage = (attacker.active_creature.sp_attack / defender_creature.sp_defense) * skill.base_damage
        
        type_factor = self._get_type_factor(skill.skill_type, defender_creature.creature_type)
        final_damage = int(raw_damage * type_factor)  # Explicitly convert to integer
        
        defender_creature.hp = max(0, defender_creature.hp - final_damage)
        self._show_text(attacker, f"{attacker.display_name}'s {attacker.active_creature.display_name} used {skill.display_name}!")
        self._show_text(defender_creature, f"{defender_creature.display_name} took {final_damage} damage!")

        if defender_creature.hp == 0:
            self._handle_knockout(defender_creature)

    def _get_type_factor(self, skill_type, creature_type):
        effectiveness = {
            ("fire", "leaf"): 2,
            ("fire", "water"): 0.5,
            ("water", "fire"): 2,
            ("water", "leaf"): 0.5,
            ("leaf", "water"): 2,
            ("leaf", "fire"): 0.5
        }
        return effectiveness.get((skill_type, creature_type), 1)

    def _handle_knockout(self, creature):
        player = self.player if creature in self.player.creatures else self.bot
        self._show_text(player, f"{player.display_name}'s {creature.display_name} was knocked out!")
        available_creatures = [c for c in player.creatures if c.hp > 0 and c != creature]
        if available_creatures:
            choices = [SelectThing(c) for c in available_creatures]
            choice = self._wait_for_choice(player, choices)
            player.active_creature = choice.thing
            self._show_text(player, f"{player.display_name} sent out {player.active_creature.display_name}!")
        else:
            self._show_text(player, f"{player.display_name} has no more creatures left!")

    def _check_battle_end(self):
        if all(c.hp == 0 for c in self.player.creatures):
            self._show_text(self.player, "You lost the battle!")
            return True
        elif all(c.hp == 0 for c in self.bot.creatures):
            self._show_text(self.player, "You won the battle!")
            return True
        return False
