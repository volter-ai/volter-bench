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

export function MainGameSceneView(props: { data: GameUIData }) {
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player?.entities.active_creature
  const opponentCreature = props.data.entities.opponent?.entities.active_creature
  const player = props.data.entities.player
  const opponent = props.data.entities.opponent

  if (!player || !opponent) {
    return null
  }

  return (
    <div className="w-full h-full aspect-video bg-gradient-to-b from-blue-100 to-blue-200">
      {/* Battlefield Area (upper 2/3) */}
      <div className="h-2/3 grid grid-cols-2 gap-4 p-4">
        {/* Top Left - Opponent Status */}
        <div className="flex items-start justify-start">
          <PlayerCard
            uid={opponent.uid}
            name={opponent.display_name}
            imageUrl={`/players/${opponent.meta.prototype_id}.png`}
          />
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl={`/creatures/${opponentCreature.meta.prototype_id}.png`}
              currentHp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Top Right - Opponent Creature */}
        <div className="flex items-center justify-center relative">
          {opponentCreature && (
            <div className="absolute bottom-0 w-48 h-48 rounded-full bg-black/10" />
          )}
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex items-center justify-center relative">
          {playerCreature && (
            <div className="absolute bottom-0 w-48 h-48 rounded-full bg-black/10" />
          )}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex items-end justify-end">
          <PlayerCard
            uid={player.uid}
            name={player.display_name}
            imageUrl={`/players/${player.meta.prototype_id}.png`}
          />
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={`/creatures/${playerCreature.meta.prototype_id}.png`}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div className="h-1/3 bg-white/80 p-4">
        <div className="flex flex-wrap gap-2 justify-center">
          {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map(skill => (
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
          ))}
          
          {/* For non-skill buttons, we use regular Button since they don't have UIDs */}
          {availableButtonSlugs.includes('back') && (
            <Button
              onClick={() => emitButtonClick('back')}
              variant="outline"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back
            </Button>
          )}

          {availableButtonSlugs.includes('swap') && (
            <Button
              onClick={() => emitButtonClick('swap')}
              variant="outline"
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
