import { useCurrentButtons } from "@/lib/useChoices.ts"
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react'
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
  meta: {
    prototype_id: string
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
    prototype_id: string
  }
  collections: {
    skills: Skill[]
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
}

interface GameUIData {
  entities: {
    player: Player
    opponent: Player
  }
}

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
    <div className="w-full h-full aspect-video bg-gradient-to-b from-blue-100 to-blue-200">
      {/* Battlefield (upper 2/3) */}
      <div className="h-2/3 grid grid-cols-2 gap-4 p-4">
        {/* Top left - Opponent Status */}
        <div className="flex items-start justify-start">
          {opponent && opponentCreature && (
            <div className="space-y-4">
              <PlayerCard
                uid={opponent.uid}
                name={opponent.display_name}
                imageUrl={`/players/${opponent.meta.prototype_id}.png`}
              />
              <CreatureCard
                uid={opponentCreature.uid}
                name={opponentCreature.display_name}
                imageUrl={`/creatures/${opponentCreature.meta.prototype_id}.png`}
                currentHp={opponentCreature.stats.hp}
                maxHp={opponentCreature.stats.max_hp}
              />
            </div>
          )}
        </div>

        {/* Top right - Opponent Creature */}
        <div className="flex items-center justify-center">
          {opponentCreature && (
            <div className="relative">
              <img 
                src={`/creatures/${opponentCreature.meta.prototype_id}_front.png`}
                alt={opponentCreature.display_name}
                className="w-48 h-48 object-contain"
              />
              <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
            </div>
          )}
        </div>

        {/* Bottom left - Player Creature */}
        <div className="flex items-center justify-center">
          {playerCreature && (
            <div className="relative">
              <img 
                src={`/creatures/${playerCreature.meta.prototype_id}_back.png`}
                alt={playerCreature.display_name}
                className="w-48 h-48 object-contain"
              />
              <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
            </div>
          )}
        </div>

        {/* Bottom right - Player Status */}
        <div className="flex items-end justify-end">
          {player && playerCreature && (
            <div className="space-y-4">
              <PlayerCard
                uid={player.uid}
                name={player.display_name}
                imageUrl={`/players/${player.meta.prototype_id}.png`}
              />
              <CreatureCard
                uid={playerCreature.uid}
                name={playerCreature.display_name}
                imageUrl={`/creatures/${playerCreature.meta.prototype_id}.png`}
                currentHp={playerCreature.stats.hp}
                maxHp={playerCreature.stats.max_hp}
              />
            </div>
          )}
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div className="h-1/3 bg-white/90 p-4 flex flex-col gap-2">
        <div className="flex gap-2 justify-center">
          {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map(skill => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              description={skill.description}
              stats={{ 
                damage: skill.stats.base_damage
              }}
            >
              <Sword className="mr-2 h-4 w-4" />
              {skill.display_name}
            </SkillButton>
          ))}
        </div>

        <div className="flex gap-2 justify-center">
          {availableButtonSlugs.map(buttonSlug => {
            if (buttonSlug === 'swap') {
              return (
                <SkillButton
                  key={buttonSlug}
                  uid={buttonSlug}
                  description="Switch to another creature"
                  stats={{}}
                >
                  <SwapHorizontal className="mr-2 h-4 w-4" />
                  Swap
                </SkillButton>
              )
            }
            if (buttonSlug === 'back') {
              return (
                <SkillButton
                  key={buttonSlug}
                  uid={buttonSlug}
                  description="Return to previous screen"
                  stats={{}}
                >
                  <ArrowLeft className="mr-2 h-4 w-4" />
                  Back
                </SkillButton>
              )
            }
            return null
          })}
        </div>
      </div>
    </div>
  )
}
