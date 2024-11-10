import { useCurrentButtons } from "@/lib/useChoices.ts"
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
    <div className="relative w-full h-full aspect-video bg-slate-50">
      {/* Battlefield Section */}
      <div className="grid grid-cols-2 grid-rows-2 h-2/3">
        {/* Opponent Status */}
        <div className="flex items-center justify-center p-4">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl={`/assets/creatures/${opponentCreature.meta.prototype_id}.png`}
              currentHp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Opponent Creature */}
        <div className="flex items-center justify-center p-4">
          <div className="relative">
            {opponentCreature && (
              <img
                src={`/assets/creatures/${opponentCreature.meta.prototype_id}.png`}
                alt={opponentCreature.display_name}
                className="w-48 h-48 object-contain"
              />
            )}
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
          </div>
        </div>

        {/* Player Creature */}
        <div className="flex items-center justify-center p-4">
          <div className="relative">
            {playerCreature && (
              <img
                src={`/assets/creatures/${playerCreature.meta.prototype_id}.png`}
                alt={playerCreature.display_name}
                className="w-48 h-48 object-contain"
              />
            )}
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full blur-sm" />
          </div>
        </div>

        {/* Player Status */}
        <div className="flex items-center justify-center p-4">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={`/assets/creatures/${playerCreature.meta.prototype_id}.png`}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* UI Section */}
      <div className="h-1/3 bg-slate-100 p-4 flex flex-col gap-4">
        <div className="flex gap-4 justify-center">
          {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map(skill => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage
              }}
              onClick={() => emitButtonClick('attack', { skillId: skill.uid })}
            >
              <Sword className="mr-2 h-4 w-4" />
              {skill.display_name}
            </SkillButton>
          ))}
        </div>
        
        <div className="flex gap-4 justify-center">
          {availableButtonSlugs.includes('back') && (
            <ClickableButton
              uid="back-button"
              onClick={() => emitButtonClick('back')}
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back
            </ClickableButton>
          )}
          
          {availableButtonSlugs.includes('swap') && (
            <ClickableButton
              uid="swap-button"
              onClick={() => emitButtonClick('swap')}
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
