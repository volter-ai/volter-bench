import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, Shield, Zap } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
  }
}

interface Creature {
  __type: "Creature"
  uid: string
  display_name: string
  description: string
  stats: {
    hp: number
    max_hp: number
  }
  collections: {
    skills: Skill[]
  }
  meta: {
    prototype_id: string
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  collections: {
    creatures: Creature[]
  }
  meta: {
    prototype_id: string
  }
}

interface GameUIData {
  entities: {
    player?: Player
    bot?: Player
    player_creature?: Creature
    bot_creature?: Creature
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const { player, bot, player_creature, bot_creature } = props.data.entities

  if (!player || !bot || !player_creature || !bot_creature) {
    return <div className="h-screen w-screen flex items-center justify-center">
      Loading game state...
    </div>
  }

  return (
    <div className="h-screen w-screen flex flex-col bg-background">
      {/* HUD */}
      <div className="w-full p-4 bg-secondary/10 flex justify-between items-center">
        {player && (
          <PlayerCard 
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/${player.meta.prototype_id}.png`}
          />
        )}
        {bot && (
          <PlayerCard 
            uid={bot.uid}
            name={bot.display_name}
            imageUrl={`/players/${bot.meta.prototype_id}.png`}
          />
        )}
      </div>

      {/* Battlefield */}
      <div className="flex-1 flex justify-between items-center px-16 py-8">
        {player_creature && (
          <div className="flex flex-col items-center gap-4">
            <CreatureCard
              uid={player_creature.uid}
              name={player_creature.display_name}
              currentHp={player_creature.stats.hp}
              maxHp={player_creature.stats.max_hp}
              imageUrl={`/creatures/${player_creature.meta.prototype_id}.png`}
            />
            <div className="text-sm font-bold text-primary">Your Creature</div>
          </div>
        )}

        {bot_creature && (
          <div className="flex flex-col items-center gap-4">
            <CreatureCard
              uid={bot_creature.uid}
              name={bot_creature.display_name}
              currentHp={bot_creature.stats.hp}
              maxHp={bot_creature.stats.max_hp}
              imageUrl={`/creatures/${bot_creature.meta.prototype_id}.png`}
            />
            <div className="text-sm font-bold text-destructive">Opponent's Creature</div>
          </div>
        )}
      </div>

      {/* Action UI */}
      <div className="w-full p-6 bg-secondary/10">
        <div className="flex flex-wrap gap-4 justify-center">
          {player_creature?.collections?.skills?.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              name={skill.display_name}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage
              }}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
