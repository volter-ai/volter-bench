import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

interface Creature {
  __type: "Creature"
  uid: string
  display_name: string
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
  const botCreature = props.data.entities.bot?.entities.active_creature

  return (
    <div className="w-full h-full aspect-[16/9] flex flex-col bg-slate-100">
      {/* Battlefield - upper 2/3 */}
      <div className="flex-grow grid grid-cols-2 gap-4 p-4">
        {/* Top left - opponent status */}
        <div className="flex justify-start items-start">
          {botCreature && (
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              hp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
              imageUrl={`/creatures/${botCreature.uid}/front.png`}
            />
          )}
        </div>

        {/* Top right - opponent creature */}
        <div className="flex justify-end items-start">
          <div className="relative w-48 h-48">
            {/* Platform shadow */}
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full" />
            {botCreature && (
              <img 
                src={`/creatures/${botCreature.uid}/front.png`}
                alt={botCreature.display_name}
                className="w-full h-full object-contain"
              />
            )}
          </div>
        </div>

        {/* Bottom left - player creature */}
        <div className="flex justify-start items-end">
          <div className="relative w-48 h-48">
            {/* Platform shadow */}
            <div className="absolute bottom-0 w-full h-4 bg-black/20 rounded-full" />
            {playerCreature && (
              <img
                src={`/creatures/${playerCreature.uid}/back.png`}
                alt={playerCreature.display_name}
                className="w-full h-full object-contain"
              />
            )}
          </div>
        </div>

        {/* Bottom right - player status */}
        <div className="flex justify-end items-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              hp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
              imageUrl={`/creatures/${playerCreature.uid}/front.png`}
            />
          )}
        </div>
      </div>

      {/* UI Area - lower 1/3 */}
      <div className="h-1/3 p-4 bg-white rounded-t-xl shadow-lg">
        <div className="grid grid-cols-2 gap-4 h-full">
          {/* Skills */}
          {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map((skill) => (
            <SkillButton
              key={skill.uid}
              uid={skill.uid}
              skillName={skill.display_name}
              description={skill.description}
              stats={{
                damage: skill.stats.base_damage
              }}
            />
          ))}

          {/* Other buttons */}
          {availableButtonSlugs.includes('back') && (
            <Button className="flex items-center gap-2">
              <ArrowLeft className="w-4 h-4" /> Back
            </Button>
          )}
          
          {availableButtonSlugs.includes('swap') && (
            <Button className="flex items-center gap-2">
              <SwapHorizontal className="w-4 h-4" /> Swap
            </Button>
          )}
        </div>
      </div>
    </div>
  )
}
