import { useCurrentButtons } from "@/lib/useChoices"
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { Button } from "@/components/ui/button"
import withClickable from "@/lib/withClickable"

const ClickableButton = withClickable(Button)

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
    [key: string]: number
  }
  meta: {
    skill_type: string
    [key: string]: any
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
    [key: string]: number
  }
  meta: {
    prototype_id: string
    creature_type: string
    [key: string]: any
  }
  collections?: {
    skills?: Skill[]
  }
}

interface Player {
  __type: "Player"
  uid: string
  display_name: string
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

  return (
    <div className="w-full h-full aspect-video bg-background flex flex-col">
      {/* Battlefield Area (upper 2/3) */}
      <div className="flex-grow grid grid-cols-2 gap-4 p-4">
        {/* Top Left - Opponent Status */}
        <div className="flex items-start justify-start">
          {opponentCreature && opponentCreature.__type === "Creature" && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl={`/creatures/${opponentCreature.meta.prototype_id}_front.png`}
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
          {playerCreature && playerCreature.__type === "Creature" && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={`/creatures/${playerCreature.meta.prototype_id}_back.png`}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* UI Area (lower 1/3) */}
      <div className="h-1/3 bg-muted p-4">
        <div className="flex flex-wrap gap-2 justify-center">
          {availableButtonSlugs.includes('attack') && 
           playerCreature?.collections?.skills?.map(skill => (
            skill.__type === "Skill" && (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage,
                  type: skill.meta.skill_type
                }}
              >
                <Sword className="mr-2 h-4 w-4" />
                {skill.display_name}
              </SkillButton>
            )
          ))}

          {availableButtonSlugs.includes('back') && (
            <ClickableButton 
              uid={`${props.data.entities.player.uid}_back`}
              variant="outline"
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back
            </ClickableButton>
          )}

          {availableButtonSlugs.includes('swap') && (
            <ClickableButton
              uid={`${props.data.entities.player.uid}_swap`}
              variant="outline"
            >
              <SwapHorizontal className="mr-2 h-4 w-4" />
              Swap
            </ClickableButton>
          )}
        </div>
      </div>
    </div>
  )
}
