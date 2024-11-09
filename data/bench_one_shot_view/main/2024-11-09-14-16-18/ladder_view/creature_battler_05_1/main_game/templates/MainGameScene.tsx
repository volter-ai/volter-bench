import { useCurrentButtons } from "@/lib/useChoices.ts"
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
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
    skill_type: string
    is_physical: boolean
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
    creature_type: string
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
    <div className="h-screen w-screen aspect-[16/9] relative bg-slate-100">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Status */}
        <div className="flex items-start justify-start p-4">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              currentHp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
              className="w-[250px]"
            />
          )}
        </div>

        {/* Opponent Creature */}
        <div className="flex items-center justify-center">
          <div className="relative w-48 h-48">
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full" />
          </div>
        </div>

        {/* Player Creature */}
        <div className="flex items-center justify-center">
          <div className="relative w-48 h-48">
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full" />
          </div>
        </div>

        {/* Player Status */}
        <div className="flex items-end justify-end p-4">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              className="w-[250px]"
            />
          )}
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 bg-white border-t-2 p-4">
        <div className="flex flex-wrap gap-2 justify-center">
          {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map(skill => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage,
                accuracy: 100 // Default value since not in data model
              }}
              variant="secondary"
              onClick={() => emitButtonClick('attack', { skillId: skill.uid })}
            >
              <Sword className="mr-2 h-4 w-4" />
              {skill.display_name}
            </SkillButton>
          ))}
          
          {availableButtonSlugs.includes('back') && (
            <Button 
              variant="outline"
              onClick={() => emitButtonClick('back')}
            >
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back
            </Button>
          )}

          {availableButtonSlugs.includes('swap') && (
            <Button 
              variant="outline"
              onClick={() => emitButtonClick('swap')}
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
