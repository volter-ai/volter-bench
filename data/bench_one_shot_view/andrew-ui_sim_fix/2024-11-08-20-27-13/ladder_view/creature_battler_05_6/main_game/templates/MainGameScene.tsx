import { useCurrentButtons } from "@/lib/useChoices.ts"
import { ArrowLeft, SwapHorizontal } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { PlayerCard } from "@/components/ui/custom/player/player_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { Button } from "@/components/ui/button"

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
  description: string
  entities: {
    active_creature?: Creature
  }
  meta: {
    prototype_id: string
  }
}

interface GameUIData {
  entities: {
    player: Player
    opponent: Player
  }
}

type ButtonSlug = 'attack' | 'back' | 'swap'

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player?.entities.active_creature
  const opponentCreature = props.data.entities.opponent?.entities.active_creature
  const player = props.data.entities.player
  const opponent = props.data.entities.opponent

  return (
    <div className="w-full h-full aspect-video bg-slate-800 flex flex-col">
      {/* Battlefield (upper 2/3) */}
      <div className="flex-grow grid grid-cols-2 gap-4 p-4">
        {/* Top left - Opponent Status */}
        <div className="flex items-start justify-start">
          {opponent && (
            <PlayerCard
              uid={opponent.uid}
              name={opponent.display_name}
              imageUrl={`/players/${opponent.meta.prototype_id}/avatar.png`}
            />
          )}
        </div>

        {/* Top right - Opponent Creature */}
        <div className="flex items-center justify-center">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl={`/creatures/${opponentCreature.meta.prototype_id}/front.png`}
              currentHp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Bottom left - Player Creature */}
        <div className="flex items-center justify-center">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={`/creatures/${playerCreature.meta.prototype_id}/back.png`}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Bottom right - Player Status */}
        <div className="flex items-end justify-end">
          {player && (
            <PlayerCard
              uid={player.uid}
              name={player.display_name}
              imageUrl={`/players/${player.meta.prototype_id}/avatar.png`}
            />
          )}
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div className="h-1/3 bg-slate-900 p-4">
        <div className="flex gap-2 flex-wrap">
          {availableButtonSlugs.includes('attack' as ButtonSlug) && 
            playerCreature?.collections.skills.map(skill => (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage
                }}
              >
                {skill.display_name}
              </SkillButton>
            ))
          }
          
          {availableButtonSlugs.includes('back' as ButtonSlug) && (
            <Button 
              onClick={() => emitButtonClick('back')}
              variant="secondary"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back
            </Button>
          )}

          {availableButtonSlugs.includes('swap' as ButtonSlug) && (
            <Button
              onClick={() => emitButtonClick('swap')}
              variant="secondary"
            >
              <SwapHorizontal className="mr-2 h-4 w-4" />
              Swap
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
