import { useCurrentButtons } from "@/lib/useChoices.ts"
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react'
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"
import { Button } from "@/components/ui/button"

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
}

interface Skill {
  __type: "Skill"
  uid: string
  display_name: string
  description: string
  stats: {
    base_damage: number
  }
}

interface Player {
  __type: "Player"
  uid: string
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
  const {
    availableButtonSlugs,
    emitButtonClick
  } = useCurrentButtons()

  const playerCreature = props.data.entities.player?.entities.active_creature
  const opponentCreature = props.data.entities.bot?.entities.active_creature

  return (
    <div className="w-full h-full aspect-video bg-gradient-to-b from-blue-100 to-blue-200">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Opponent Status */}
        <div className="flex justify-start items-center">
          {opponentCreature && (
            <CreatureCard
              uid={opponentCreature.uid}
              name={opponentCreature.display_name}
              imageUrl={`/creatures/${opponentCreature.uid}/front.png`}
              currentHp={opponentCreature.stats.hp}
              maxHp={opponentCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Opponent Creature */}
        <div className="flex justify-end items-center">
          <div className="w-48 h-48 relative">
            {/* Platform shadow */}
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full" />
          </div>
        </div>

        {/* Player Creature */}
        <div className="flex justify-start items-center">
          <div className="w-48 h-48 relative">
            {/* Platform shadow */}
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full" />
          </div>
        </div>

        {/* Player Status */}
        <div className="flex justify-end items-center">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              imageUrl={`/creatures/${playerCreature.uid}/back.png`}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 bg-white/80 p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map(skill => (
            skill.__type === 'Skill' && (
              <SkillButton
                key={skill.uid}
                uid={skill.uid}
                skillName={skill.display_name}
                description={skill.description}
                stats={{
                  damage: skill.stats.base_damage
                }}
              />
            )
          ))}
          
          {availableButtonSlugs.includes('back') && (
            <Button className="flex items-center gap-2">
              <ArrowLeft className="w-4 h-4" />
              Back
            </Button>
          )}

          {availableButtonSlugs.includes('swap') && (
            <Button className="flex items-center gap-2">
              <SwapHorizontal className="w-4 h-4" />
              Swap
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
