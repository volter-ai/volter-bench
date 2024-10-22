attacker = action[1].active_creature
   defender = self.bot.active_creature if action[1] == self.player else self.player.active_creature
   self.perform_attack(attacker, defender, action[2])
