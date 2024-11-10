import { useCurrentButtons } from "@/lib/useChoices.ts";
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
    <div className="h-screen w-screen aspect-[16/9] bg-gradient-to-b from-blue-100 to-blue-200">
      {/* Battlefield Section */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Top Left - Opponent Status */}
        <div className="flex items-start justify-start">
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

        {/* Top Right - Opponent Creature */}
        <div className="flex items-center justify-center">
          {/* Creature image would be rendered here */}
        </div>

        {/* Bottom Left - Player Creature */}
        <div className="flex items-center justify-center">
          {/* Creature image would be rendered here */}
        </div>

        {/* Bottom Right - Player Status */}
        <div className="flex items-end justify-end">
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

      {/* UI Section */}
      <div className="h-1/3 bg-white/90 p-4 flex flex-col gap-4">
        <div className="grid grid-cols-2 gap-4">
          {/* Skills */}
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

        <div className="flex gap-4 justify-end">
          {availableButtonSlugs.includes('swap') && (
            <Button>
              <SwapHorizontal className="mr-2 h-4 w-4" />
              Swap
            </Button>
          )}
          
          {availableButtonSlugs.includes('back') && (
            <Button>
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
