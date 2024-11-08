import { useCurrentButtons } from "@/lib/useChoices.ts";
import { Sword, ArrowLeft, SwapHorizontal } from 'lucide-react'
import { Button } from "@/components/ui/button"
import { CreatureCard } from "@/components/ui/custom/creature/creature_card"
import { SkillButton } from "@/components/ui/custom/skill/skill_button"

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
  display_name: string
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
    <div className="w-full h-full aspect-w-16 aspect-h-9 bg-gradient-to-b from-sky-400 to-sky-600">
      {/* Battlefield Area */}
      <div className="h-2/3 grid grid-cols-2 grid-rows-2 gap-4 p-4">
        {/* Bot Status */}
        <div className="flex items-start justify-start">
          {botCreature && (
            <CreatureCard
              uid={botCreature.uid}
              name={botCreature.display_name}
              image={`/creatures/${botCreature.uid}/front.png`}
              currentHp={botCreature.stats.hp}
              maxHp={botCreature.stats.max_hp}
            />
          )}
        </div>

        {/* Bot Creature */}
        <div className="flex items-center justify-center">
          {/* Creature image would be rendered here */}
        </div>

        {/* Player Creature */}
        <div className="flex items-center justify-center">
          {/* Creature image would be rendered here */}
        </div>

        {/* Player Status */}
        <div className="flex items-end justify-end">
          {playerCreature && (
            <CreatureCard
              uid={playerCreature.uid}
              name={playerCreature.display_name}
              image={`/creatures/${playerCreature.uid}/back.png`}
              currentHp={playerCreature.stats.hp}
              maxHp={playerCreature.stats.max_hp}
            />
          )}
        </div>
      </div>

      {/* UI Area */}
      <div className="h-1/3 bg-white/90 rounded-t-xl p-4">
        <div className="grid grid-cols-2 grid-rows-2 gap-4 h-full">
          {availableButtonSlugs.includes('attack') && playerCreature?.collections.skills.map(skill => (
            skill.__type === "Skill" && (
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
