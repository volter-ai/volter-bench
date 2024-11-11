import { useCurrentButtons } from "@/lib/useChoices.ts"
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { SwapHorizontal } from 'lucide-react'

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
  }
  meta: {
    image_url?: string
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
  meta: {
    image_url?: string
  }
  collections: {
    skills: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
  meta: {
    image_url?: string
  }
  entities: {
    active_creature?: Creature
  }
}

interface GameUIData {
  entities: {
    player: Player
    bot: Player
  }
}

export function MainGameSceneView(props: { data: GameUIData }) {
  const { availableButtonSlugs, emitButtonClick } = useCurrentButtons()

  const playerCreature = props.data.entities.player?.entities.active_creature
  const botCreature = props.data.entities.bot?.entities.active_creature
  const player = props.data.entities.player
  const bot = props.data.entities.bot

  return (
    <div className="w-full h-full aspect-video bg-slate-800 flex flex-col">
      {/* Battlefield Area (upper 2/3) */}
      <div className="flex-grow grid grid-cols-2 grid-rows-2 p-4 gap-4">
        {/* Top Left - Bot Status */}
        <div className="flex items-start justify-start">
          {bot && (
            <PlayerCard
              uid={bot.uid}
              name={bot.display_name}
              imageUrl={bot.meta.image_url || '/placeholder.png'}
            />
          )}
        </div>

        {/* Top Right - Bot Creature */}
        <div className="flex items-center justify-center">
          {botCreature && (
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              image={botCreature.meta.image_url || '/placeholder.png'}
              currentHp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex items-center justify-center">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image={playerCreature.meta.image_url || '/placeholder.png'}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex items-end justify-end">
          {player && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl={player.meta.image_url || '/placeholder.png'}
            />
          )}
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div className="h-1/3 bg-slate-700 p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {availableButtonSlugs.includes('attack') && 
            playerCreature?.collections.skills.map((skill) => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                name={skill.display_name}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage
                }}
              />
            ))
          }
          
          {availableButtonSlugs.includes('swap') && (
            <button
              className="flex items-center justify-center gap-2 bg-slate-600 rounded-lg hover:bg-slate-500"
              onClick={() => emitButtonClick('swap')}
            >
              <SwapHorizontal className="w-6 h-6" />
              Swap Creature
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
